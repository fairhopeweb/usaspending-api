from abc import ABCMeta
from collections import Counter
from decimal import Decimal
from enum import Enum
from typing import Dict, List

from django.db.models import F, QuerySet, TextField
from django.db.models.functions import Concat

from usaspending_api.recipient.models import StateData
from usaspending_api.references.abbreviations import code_to_state, fips_to_code
from usaspending_api.references.models import PopCongressionalDistrict, PopCounty, RefCountryCode
from usaspending_api.search.helpers.spending_by_category_helpers import (
    fetch_country_name_from_code,
    fetch_state_name_from_code,
)
from usaspending_api.search.v2.views.spending_by_category_views.spending_by_category import (
    AbstractSpendingByCategoryViewSet,
    Category,
)


class LocationType(Enum):
    COUNTRY = "country"
    STATE_TERRITORY = "state"
    COUNTY = "county"
    CONGRESSIONAL_DISTRICT = "congressional"


def _combine_dicts_by_keys(dicts, keys, sum_key) -> List[Dict]:
    """Combine all dictionaries in a list that have the same values for the given field(s)

    Args:
        dicts (list[dict]): List of dictionaries that may contain duplicate values.
        keys (list[str]): List of keys to check the values of in each dictionary.
            If ALL of the values for these keys are the same between dictionaries, then they
            will be combined into one dictionary.
        sum_key (str): A key within the duplicate dictionaries that will be summed together.

    Returns:
        List[Dict]: List of dictionaries, after combining and summing any duplicate dictionaries

    Example:
        [
            {'id': None, 'code': '01', 'name': 'ID-01', 'amount': Decimal('74338979.79')},
            {'id': None, 'code': '02', 'name': 'ID-02', 'amount': Decimal('32381356.49')},
            {'id': None, 'code': None, 'name': None, 'amount': Decimal('6952030.82')},
            {'id': None, 'code': None, 'name': None, 'amount': Decimal('645582')},
            {'id': None, 'code': None, 'name': None, 'amount': Decimal('4324')}
        ]

        becomes this after combing the last 3 dictionaries because the `code` and `name` keys are the same:
        [
            {'id': None, 'code': '01', 'name': 'ID-01', 'amount': Decimal('74338979.79')},
            {'id': None, 'code': '02', 'name': 'ID-02', 'amount': Decimal('32381356.49')},
            {'id': None, 'code': None, 'name': None, 'amount': Decimal('7601936.82')},
        ]
    """
    combined_dicts = {}

    for d in dicts:
        key = tuple(d[key] for key in keys)
        if key not in combined_dicts:
            combined_dicts[key] = d.copy()
        else:
            combined_dicts[key][sum_key] += d[sum_key]

    return list(combined_dicts.values())


class AbstractLocationViewSet(AbstractSpendingByCategoryViewSet, metaclass=ABCMeta):
    """
    Base class used by the different spending by Location endpoints
    """

    location_type: LocationType

    def build_elasticsearch_result(self, response: dict) -> List[dict]:
        def _key_to_geo_code(key):
            if self.location_type == LocationType.COUNTRY:
                return key
            return f"{code_to_state[key[:2]]['fips']}{key[2:]}" if (key and key[:2] in code_to_state) else None

        # Get the codes
        location_info_buckets = response.get("group_by_agg_key", {}).get("buckets", [])
        code_list = [_key_to_geo_code(bucket["key"]) for bucket in location_info_buckets if bucket.get("key")]

        # Get the current location info
        current_location_info = {}
        if self.location_type == LocationType.COUNTRY:
            location_info_query = (
                RefCountryCode.objects.annotate(shape_code=F("country_code"))
                .filter(country_code__in=code_list)
                .annotate(name=F("country_name"), code=F("country_code"))
                .values("shape_code", "name", "code")
            )
        elif self.location_type == LocationType.STATE_TERRITORY:
            location_info_query = (
                StateData.objects.annotate(shape_code=F("fips"))
                .filter(shape_code__in=code_list)
                .values("shape_code", "name", "code")
            )
        elif self.location_type == LocationType.COUNTY:
            location_info_query = (
                PopCounty.objects.annotate(
                    shape_code=Concat(F("state_code"), F("county_number"), output_format=TextField())
                )
                .filter(shape_code__in=code_list)
                .annotate(name=F("county_name"), code=F("county_number"))
                .values("shape_code", "name", "code")
            )
        elif self.location_type == LocationType.CONGRESSIONAL_DISTRICT:
            # Get all `shape_code`, `state_code`, and `congressional_district` values for the given state
            location_info_query = (
                PopCongressionalDistrict.objects.annotate(
                    shape_code=Concat(F("state_code"), F("congressional_district"), output_field=TextField())
                )
                .filter(state_code__in={sc[:2] for sc in code_list})
                .values("shape_code", "state_code", "congressional_district")
            )

            # Add the `90` congressional code to the list of valid codes, if the given state has more
            #   than 1 congressional district
            counts = Counter([state["state_code"] for state in location_info_query.all()])
            for state_code, occurrences in counts.items():
                if occurrences > 1:
                    current_location_info[f"{state_code}90"] = {
                        "state_code": state_code,
                        "congressional_district": "90",
                    }

            # can't do the distict transformation in the queryset, see below
        for location_info in location_info_query.all():
            shape_code = location_info.pop("shape_code")
            current_location_info[shape_code] = location_info

        # Build out the results
        results = []
        for bucket in location_info_buckets:
            key = _key_to_geo_code(bucket.get("key"))
            location_info = current_location_info.get(key) or {}

            if location_info:
                if self.location_type == LocationType.CONGRESSIONAL_DISTRICT:
                    location_info["code"] = location_info.get("congressional_district") or ""
                    display_code = "MULTIPLE DISTRICTS" if location_info["code"] == "90" else location_info["code"]
                    location_info["name"] = f"{fips_to_code.get(location_info['state_code'], '')}-{display_code}"
                elif self.location_type == LocationType.STATE_TERRITORY:
                    location_info["name"] = location_info["name"].title()
                else:
                    location_info["name"] = location_info["name"].upper()

            results.append(
                {
                    "id": None,
                    "code": location_info.get("code"),
                    "name": location_info.get("name"),
                    "amount": int(bucket.get("sum_field", {"value": 0})["value"]) / Decimal("100"),
                }
            )

        # Combine all dicts in the `results` list that have the same values for `code` and `name`and sum their `amount`
        # values together. These fields can be `None` if they don't match an entry in the ref_population_cong_district
        # table.
        if self.location_type == LocationType.CONGRESSIONAL_DISTRICT:
            results = _combine_dicts_by_keys(results, ["code", "name"], "amount")

        return results

    def query_django_for_subawards(self, base_queryset: QuerySet) -> List[dict]:
        subaward_mappings = {
            LocationType.COUNTY: "sub_place_of_perform_county_code",
            LocationType.CONGRESSIONAL_DISTRICT: "sub_place_of_perform_congressio",
            LocationType.STATE_TERRITORY: "sub_place_of_perform_state_code",
            LocationType.COUNTRY: "sub_place_of_perform_country_co",
        }
        django_filters = {f"{subaward_mappings[self.location_type]}__isnull": False}

        if self.location_type == LocationType.COUNTY:
            django_values = [
                "sub_place_of_perform_country_co",
                "sub_place_of_perform_state_code",
                "sub_place_of_perform_county_code",
                "sub_place_of_perform_county_name",
            ]
            annotations = {"code": F("sub_place_of_perform_county_code"), "name": F("sub_place_of_perform_county_name")}
        elif self.location_type == LocationType.CONGRESSIONAL_DISTRICT:
            django_values = [
                "sub_place_of_perform_country_co",
                "sub_place_of_perform_state_code",
                "sub_place_of_perform_congressio",
            ]
            annotations = {"code": F("sub_place_of_perform_congressio")}
        elif self.location_type == LocationType.STATE_TERRITORY:
            django_values = ["sub_place_of_perform_country_co", "sub_place_of_perform_state_code"]
            annotations = {"code": F("sub_place_of_perform_state_code")}
        else:
            django_values = ["sub_place_of_perform_country_co"]
            annotations = {"code": F("sub_place_of_perform_country_co")}

        queryset = self.common_db_query(base_queryset, django_filters, django_values).annotate(**annotations)
        lower_limit = self.pagination.lower_limit
        upper_limit = self.pagination.upper_limit
        query_results = list(queryset[lower_limit:upper_limit])

        for row in query_results:
            row["id"] = None
            if self.location_type == LocationType.CONGRESSIONAL_DISTRICT:
                district_code = row["code"]
                if district_code == "90":
                    district_code = "MULTIPLE DISTRICTS"
                row["name"] = f"{row['sub_place_of_perform_state_code']}-{district_code}"
            elif self.location_type == LocationType.COUNTRY:
                row["name"] = fetch_country_name_from_code(row["code"])
            elif self.location_type == LocationType.STATE_TERRITORY:
                row["name"] = fetch_state_name_from_code(row["code"])

            for key in django_values:
                row.pop(key)

        return query_results


class CountyViewSet(AbstractLocationViewSet):
    """
    This route takes award filters and returns spending by County.
    """

    endpoint_doc = "usaspending_api/api_contracts/contracts/v2/search/spending_by_category/county.md"

    location_type = LocationType.COUNTY
    category = Category(name="county", agg_key="pop_county_agg_key")


class DistrictViewSet(AbstractLocationViewSet):
    """
    This route takes award filters and returns spending by Congressional District.
    """

    endpoint_doc = "usaspending_api/api_contracts/contracts/v2/search/spending_by_category/district.md"

    location_type = LocationType.CONGRESSIONAL_DISTRICT
    category = Category(name="district", agg_key="pop_congressional_agg_key")


class StateTerritoryViewSet(AbstractLocationViewSet):
    """
    This route takes award filters and returns spending by State Territory.
    """

    endpoint_doc = "usaspending_api/api_contracts/contracts/v2/search/spending_by_category/state_territory.md"

    location_type = LocationType.STATE_TERRITORY
    category = Category(name="state_territory", agg_key="pop_state_agg_key")


class CountryViewSet(AbstractLocationViewSet):
    """
    This route takes award filters and returns spending by Country.
    """

    endpoint_doc = "usaspending_api/api_contracts/contracts/v2/search/spending_by_category/country.md"

    location_type = LocationType.COUNTRY
    category = Category(name="country", agg_key="pop_country_agg_key")
