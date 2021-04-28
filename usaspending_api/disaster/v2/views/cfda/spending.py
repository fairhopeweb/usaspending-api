from typing import List

from usaspending_api.disaster.v2.views.elasticsearch_base import (
    ElasticsearchDisasterBase,
    ElasticsearchSpendingPaginationMixin,
)
from usaspending_api.references.models import Cfda
from usaspending_api.search.v2.elasticsearch_helper import get_summed_value_as_float


class CfdaSpendingViewSet(ElasticsearchSpendingPaginationMixin, ElasticsearchDisasterBase):
    """
    This route takes DEF Codes, Award Type Codes, and Query text and returns Spending of CFDA.
    """

    endpoint_doc = "usaspending_api/api_contracts/contracts/v2/disaster/cfda/spending.md"

    required_filters = ["def_codes", "_assistance_award_type_codes", "query"]
    query_fields = ["cfda_title.contains", "cfda_number.contains"]
    agg_key = "cfda_number.keyword"

    def build_elasticsearch_result(self, info_buckets: List[dict]) -> List[dict]:
        results = []

        cfda_prefetch_pks = [bucket.get("key") for bucket in info_buckets]
        prefetched_cfdas = {
            cfda["program_number"]: cfda for cfda in Cfda.objects.filter(program_number__in=cfda_prefetch_pks).values()
        }

        for bucket in info_buckets:
            cfda_number = bucket.get("key")
            cfda = prefetched_cfdas.get(cfda_number, {})

            results.append(
                {
                    "id": cfda.get("id"),
                    "code": cfda.get("program_number"),
                    "description": cfda.get("program_title"),
                    "award_count": int(bucket.get("doc_count", 0)),
                    "resource_link": cfda.get("url") if cfda.get("url") != "None;" else None,
                    "cfda_federal_agency": cfda.get("federal_agency"),
                    "cfda_objectives": cfda.get("objectives"),
                    "cfda_website": cfda.get("website_address"),
                    "applicant_eligibility": cfda.get("applicant_eligibility"),
                    "beneficiary_eligibility": cfda.get("beneficiary_eligibility"),
                    **{
                        column: get_summed_value_as_float(bucket.get("nested", {}), self.sum_column_mapping[column])
                        for column in self.sum_column_mapping
                    },
                }
            )

        return results
