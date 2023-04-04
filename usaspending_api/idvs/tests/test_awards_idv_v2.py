import json
import pytest

from model_bakery import baker
from rest_framework import status

from usaspending_api.references.models import ToptierAgency, SubtierAgency


@pytest.fixture
def awards_and_transactions(db):

    subag = {"pk": 1, "name": "agency name", "abbreviation": "some other stuff"}
    baker.make("references.SubtierAgency", subtier_code="def", **subag)
    baker.make("references.ToptierAgency", toptier_code="abc", **subag)

    duns = {"awardee_or_recipient_uniqu": "123", "uei": "ABC", "legal_business_name": "Sams Club"}
    parent_recipient_lookup = {"duns": "123", "uei": "ABC", "recipient_hash": "cfd3f3f5-2162-7679-9f6b-429cecaa3e1e"}
    recipient_lookup = {"duns": "456", "uei": "DEF", "recipient_hash": "66545a8d-bf37-3eda-cce5-29c6170c9aab"}
    parent_recipient_profile = {"recipient_hash": "cfd3f3f5-2162-7679-9f6b-429cecaa3e1e", "recipient_level": "P"}
    recipient_profile = {"recipient_hash": "66545a8d-bf37-3eda-cce5-29c6170c9aab", "recipient_level": "C"}
    baker.make("references.Cfda", program_number=1234)
    baker.make("recipient.DUNS", **duns)
    baker.make("recipient.RecipientLookup", **parent_recipient_lookup)
    baker.make("recipient.RecipientLookup", **recipient_lookup)
    baker.make("recipient.RecipientProfile", **parent_recipient_profile)
    baker.make("recipient.RecipientProfile", **recipient_profile)

    ag = {"pk": 1, "toptier_agency": ToptierAgency.objects.get(pk=1), "subtier_agency": SubtierAgency.objects.get(pk=1)}
    baker.make("references.Agency", **ag)

    baker.make("references.PSC", code="4730", description="HOSE, PIPE, TUBE, LUBRICATION, AND RAILING FITTINGS")
    baker.make("references.PSC", code="47", description="PIPE, TUBING, HOSE, AND FITTINGS")

    baker.make("references.NAICS", code="333911", description="PUMP AND PUMPING EQUIPMENT MANUFACTURING")
    baker.make("references.NAICS", code="3339", description="Other General Purpose Machinery Manufacturing")
    baker.make("references.NAICS", code="33", description="Manufacturing")

    award_1_model = {
        "award_id": 1,
        "latest_transaction_id": 1,
        "type": "IDV_B_B",
        "category": "idv",
        "piid": 1234,
        "type_description": "INDEFINITE DELIVERY / INDEFINITE QUANTITY",
        "description": "lorem ipsum",
        "generated_unique_award_id": "ASST_AGG_1830212.0481163_3620",
        "total_subaward_amount": 12345.00,
        "subaward_count": 10,
        "awarding_agency_id": 1,
        "funding_agency_id": 1,
        "date_signed": "2005-04-03",
        "action_date": "2020-01-01",
    }
    award_2_model = {
        "award_id": 2,
        "latest_transaction_id": 2,
        "type": "IDV_A",
        "type_description": "GWAC",
        "category": "idv",
        "piid": "5678",
        "parent_award_piid": "1234",
        "description": "lorem ipsum",
        "awarding_agency_id": 1,
        "funding_agency_id": 1,
        "total_obligation": 1000,
        "base_and_all_options_value": 2000,
        "period_of_performance_start_date": "2004-02-04",
        "period_of_performance_current_end_date": "2005-02-04",
        "generated_unique_award_id": "CONT_AWD_03VD_9700_SPM30012D3486_9700",
        "total_subaward_amount": 12345.00,
        "subaward_count": 10,
        "date_signed": "2004-03-02",
        "officer_1_name": "Tom",
        "officer_1_amount": 10000.00,
        "officer_2_name": "Stan Burger",
        "officer_2_amount": 1234.00,
        "action_date": "2020-01-01",
    }
    award_3_model = {
        "award_id": 3,
        "latest_transaction_id": 3,
        "type": "IDV_A",
        "type_description": "GWAC",
        "category": "idv",
        "piid": "9123",
        "parent_award_piid": "1234",
        "description": "lorem ipsum",
        "awarding_agency_id": 1,
        "funding_agency_id": 1,
        "total_obligation": 1000,
        "base_and_all_options_value": 2000,
        "period_of_performance_start_date": "2004-02-04",
        "period_of_performance_current_end_date": "2005-02-04",
        "generated_unique_award_id": "CONT_AWD_03VD_9700_SPM30012D3486_9800",
        "total_subaward_amount": 12345.00,
        "subaward_count": 10,
        "date_signed": "2004-03-02",
        "action_date": "2020-01-01",
    }
    baker.make("search.AwardSearch", **award_1_model)
    baker.make("search.AwardSearch", **award_2_model)
    baker.make("search.AwardSearch", **award_3_model)

    asst_data = {"is_fpds": False, "transaction_id": 1, "award_id": 1, "cfda_number": 1234, "cfda_title": "farms"}
    baker.make("search.TransactionSearch", **asst_data)

    latest_transaction_contract_data = {
        "action_date": "2010-01-01",
        "agency_id": "192",
        "award_id": 2,
        "recipient_name": "John's Pizza",
        "recipient_name_raw": "John's Pizza",
        "recipient_uei": "DEF",
        "recipient_unique_id": "456",
        "business_categories": ["small_business"],
        "clinger_cohen_act_planning": None,
        "clinger_cohen_act_pla_desc": "NO",
        "commercial_item_acquisitio": "A",
        "commercial_item_acqui_desc": None,
        "commercial_item_test_progr": None,
        "commercial_item_test_desc": "NO",
        "consolidated_contract": None,
        "consolidated_contract_desc": "NOT CONSOLIDATED",
        "construction_wage_rate_req": None,
        "construction_wage_rat_desc": "NO",
        "cost_or_pricing_data": None,
        "cost_or_pricing_data_desc": "NO",
        "program_system_or_equipmen": "000",
        "program_system_or_equ_desc": None,
        "dod_claimant_program_code": None,
        "dod_claimant_prog_cod_desc": "C9E",
        "domestic_or_foreign_entity": None,
        "domestic_or_foreign_e_desc": "U.S. OWNED BUSINESS",
        "evaluated_preference": None,
        "evaluated_preference_desc": "NO PREFERENCE USED",
        "extent_competed": "D",
        "extent_compete_description": None,
        "fair_opportunity_limited_s": None,
        "fair_opportunity_limi_desc": None,
        "fed_biz_opps": None,
        "fed_biz_opps_description": "YES",
        "foreign_funding": None,
        "foreign_funding_desc": "NOT APPLICABLE",
        "idv_type_description": "IDC",
        "information_technology_com": None,
        "information_technolog_desc": "NOT IT PRODUCTS OR SERVICES",
        "interagency_contracting_au": None,
        "interagency_contract_desc": "NOT APPLICABLE",
        "is_fpds": True,
        "labor_standards": None,
        "labor_standards_descrip": "NO",
        "last_modified_date": "2018-08-24",
        "legal_entity_address_line1": "123 main st",
        "legal_entity_address_line2": None,
        "legal_entity_address_line3": None,
        "recipient_location_city_name": "Charlotte",
        "recipient_location_congressional_code": "90",
        "recipient_location_country_code": "USA",
        "recipient_location_country_name": "UNITED STATES",
        "recipient_location_county_name": "BUNCOMBE",
        "recipient_location_state_code": "NC",
        "recipient_location_state_name": "North Carolina",
        "recipient_location_zip5": "12204",
        "legal_entity_zip_last4": "5312",
        "major_program": None,
        "materials_supplies_article": None,
        "materials_supplies_descrip": "NO",
        "multi_year_contract": None,
        "multi_year_contract_desc": "NO",
        "multiple_or_single_aw_desc": "MULTIPLE AWARD",
        "naics_code": "333911",
        "naics_description": "PUMP AND PUMPING EQUIPMENT MANUFACTURING",
        "national_interest_action": "H2020K",
        "national_interest_desc": "HURRICANE KIRK",
        "number_of_offers_received": None,
        "ordering_period_end_date": "2025-06-30",
        "other_than_full_and_open_c": None,
        "other_than_full_and_o_desc": None,
        "parent_award_id": "1",
        "period_of_perf_potential_e": "2003-04-05",
        "period_of_performance_start_date": "2010-09-23",
        "piid": "0",
        "pk": 2,
        "pop_country_name": "Pacific Delta Amazon",
        "pop_city_name": "Austin",
        "pop_country_code": "PDA",
        "pop_county_name": "Tripoli",
        "place_of_perform_zip_last4": "2135",
        "pop_congressional_code": "-0-",
        "pop_state_code": "TX",
        "pop_zip5": "40221",
        "price_evaluation_adjustmen": None,
        "product_or_service_code": "4730",
        "product_or_service_description": None,
        "program_acronym": None,
        "purchase_card_as_payment_m": None,
        "purchase_card_as_paym_desc": "NO",
        "referenced_idv_agency_iden": "168",
        "referenced_idv_agency_desc": "whatever",
        "sea_transportation": None,
        "sea_transportation_desc": "NO",
        "small_business_competitive": "False",
        "solicitation_identifier": None,
        "solicitation_procedures": "NP",
        "solicitation_procedur_desc": None,
        "subcontracting_plan": "B",
        "subcontracting_plan_desc": None,
        "transaction_id": 2,
        "type_of_contract_pricing": None,
        "type_of_contract_pric_desc": "FIRM FIXED PRICE",
        "type_of_idc_description": "INDEFINITE DELIVERY / INDEFINITE QUANTITY",
        "type_set_aside": None,
        "type_set_aside_description": None,
        "parent_recipient_name": "Dave's Pizza LLC",
        "parent_recipient_name_raw": "Dave's Pizza LLC",
        "parent_uei": "ABC",
        "parent_recipient_unique_id": "123",
        "awarding_office_name": "awarding_office",
        "funding_office_name": "funding_office",
        "officer_1_name": "Tom",
        "officer_1_amount": 10000.00,
        "officer_2_name": "Stan Burger",
        "officer_2_amount": 1234.00,
    }
    latest_transaction_contract_data_without_recipient_name_or_id = {
        "action_date": "2020-01-01",
        "agency_id": "192",
        "award_id": 3,
        "recipient_name": None,
        "recipient_name_raw": None,
        "recipient_uei": None,
        "recipient_unique_id": None,
        "business_categories": ["small_business"],
        "clinger_cohen_act_planning": None,
        "clinger_cohen_act_pla_desc": "NO",
        "commercial_item_acquisitio": "A",
        "commercial_item_acqui_desc": None,
        "commercial_item_test_progr": None,
        "commercial_item_test_desc": "NO",
        "consolidated_contract": None,
        "consolidated_contract_desc": "NOT CONSOLIDATED",
        "construction_wage_rate_req": None,
        "construction_wage_rat_desc": "NO",
        "cost_or_pricing_data": None,
        "cost_or_pricing_data_desc": "NO",
        "program_system_or_equipmen": "000",
        "program_system_or_equ_desc": None,
        "dod_claimant_program_code": None,
        "dod_claimant_prog_cod_desc": "C9E",
        "domestic_or_foreign_entity": None,
        "domestic_or_foreign_e_desc": "U.S. OWNED BUSINESS",
        "evaluated_preference": None,
        "evaluated_preference_desc": "NO PREFERENCE USED",
        "extent_competed": "D",
        "extent_compete_description": None,
        "fair_opportunity_limited_s": None,
        "fair_opportunity_limi_desc": None,
        "fed_biz_opps": None,
        "fed_biz_opps_description": "YES",
        "foreign_funding": None,
        "foreign_funding_desc": "NOT APPLICABLE",
        "idv_type_description": "IDC",
        "information_technology_com": None,
        "information_technolog_desc": "NOT IT PRODUCTS OR SERVICES",
        "interagency_contracting_au": None,
        "interagency_contract_desc": "NOT APPLICABLE",
        "is_fpds": True,
        "labor_standards": None,
        "labor_standards_descrip": "NO",
        "last_modified_date": "2018-08-24",
        "legal_entity_address_line1": "123 main st",
        "legal_entity_address_line2": None,
        "legal_entity_address_line3": None,
        "recipient_location_city_name": "Charlotte",
        "recipient_location_congressional_code": "90",
        "recipient_location_country_code": "USA",
        "recipient_location_country_name": "UNITED STATES",
        "recipient_location_county_name": "BUNCOMBE",
        "recipient_location_state_code": "NC",
        "recipient_location_state_name": "North Carolina",
        "recipient_location_zip5": "12204",
        "legal_entity_zip_last4": "5312",
        "major_program": None,
        "materials_supplies_article": None,
        "materials_supplies_descrip": "NO",
        "multi_year_contract": None,
        "multi_year_contract_desc": "NO",
        "multiple_or_single_aw_desc": "MULTIPLE AWARD",
        "naics_code": "333911",
        "naics_description": "PUMP AND PUMPING EQUIPMENT MANUFACTURING",
        "number_of_offers_received": None,
        "ordering_period_end_date": "2025-06-30",
        "other_than_full_and_open_c": None,
        "other_than_full_and_o_desc": None,
        "parent_award_id": "1",
        "period_of_perf_potential_e": "2003-04-05",
        "period_of_performance_start_date": "2010-09-23",
        "piid": "0",
        "pk": 3,
        "pop_country_name": "Pacific Delta Amazon",
        "pop_city_name": "Austin",
        "pop_country_code": "PDA",
        "pop_county_name": "Tripoli",
        "place_of_perform_zip_last4": "2135",
        "pop_congressional_code": "-0-",
        "pop_state_code": "TX",
        "pop_zip5": "40221",
        "price_evaluation_adjustmen": None,
        "product_or_service_code": "4730",
        "product_or_service_description": None,
        "program_acronym": None,
        "purchase_card_as_payment_m": None,
        "purchase_card_as_paym_desc": "NO",
        "referenced_idv_agency_iden": "168",
        "referenced_idv_agency_desc": "whatever",
        "sea_transportation": None,
        "sea_transportation_desc": "NO",
        "small_business_competitive": "False",
        "solicitation_identifier": None,
        "solicitation_procedures": "NP",
        "solicitation_procedur_desc": None,
        "subcontracting_plan": "B",
        "subcontracting_plan_desc": None,
        "transaction_id": 3,
        "type_of_contract_pricing": None,
        "type_of_contract_pric_desc": "FIRM FIXED PRICE",
        "type_of_idc_description": "INDEFINITE DELIVERY / INDEFINITE QUANTITY",
        "type_set_aside": None,
        "type_set_aside_description": None,
        "parent_recipient_name": None,
        "parent_recipient_name_raw": None,
        "parent_uei": None,
        "parent_recipient_unique_id": None,
        "awarding_office_name": "awarding_office",
        "funding_office_name": "funding_office",
    }
    baker.make("search.TransactionSearch", **latest_transaction_contract_data)
    baker.make("search.TransactionSearch", **latest_transaction_contract_data_without_recipient_name_or_id)


@pytest.mark.django_db
def test_no_data_idv_award_endpoint(client):
    """Test the /v2/awards endpoint."""

    resp = client.get("/api/v2/awards/27254436/", content_type="application/json")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_award_endpoint_different_ids(client, awards_and_transactions):
    resp = client.get("/api/v2/awards/CONT_AWD_03VD_9700_SPM30012D3486_9700/", content_type="application/json")
    assert resp.status_code == status.HTTP_200_OK
    assert json.loads(resp.content.decode("utf-8")) == expected_response_idv

    resp = client.get("/api/v2/awards/2/", content_type="application/json")
    assert resp.status_code == status.HTTP_200_OK
    assert json.loads(resp.content.decode("utf-8")) == expected_response_idv


def test_award_endpoint_for_null_recipient_information(client, awards_and_transactions):
    resp = client.get("/api/v2/awards/3/", content_type="application/json")
    assert resp.status_code == status.HTTP_200_OK
    assert json.loads(resp.content.decode("utf-8")).get("recipient") == recipient_without_id_and_name


expected_response_idv = {
    "id": 2,
    "type": "IDV_A",
    "generated_unique_award_id": "CONT_AWD_03VD_9700_SPM30012D3486_9700",
    "category": "idv",
    "type_description": "GWAC",
    "piid": "5678",
    "parent_award": None,
    "description": "lorem ipsum",
    "period_of_performance": {
        "start_date": "2004-02-04",
        "end_date": "2025-06-30",
        "last_modified_date": "2018-08-24",
        "potential_end_date": "2003-04-05",
    },
    "awarding_agency": {
        "id": 1,
        "has_agency_page": False,
        "toptier_agency": {"name": "agency name", "abbreviation": "some other stuff", "code": "abc", "slug": None},
        "subtier_agency": {"name": "agency name", "abbreviation": "some other stuff", "code": "def"},
        "office_agency_name": "awarding_office",
    },
    "funding_agency": {
        "id": 1,
        "has_agency_page": False,
        "toptier_agency": {"name": "agency name", "abbreviation": "some other stuff", "code": "abc", "slug": None},
        "subtier_agency": {"name": "agency name", "abbreviation": "some other stuff", "code": "def"},
        "office_agency_name": "funding_office",
    },
    "recipient": {
        "recipient_hash": "66545a8d-bf37-3eda-cce5-29c6170c9aab-C",
        "recipient_name": "John's Pizza",
        "recipient_uei": "DEF",
        "recipient_unique_id": "456",
        "parent_recipient_hash": "cfd3f3f5-2162-7679-9f6b-429cecaa3e1e-P",
        "parent_recipient_name": "Dave's Pizza LLC",
        "parent_recipient_uei": "ABC",
        "parent_recipient_unique_id": "123",
        "business_categories": ["Small Business"],
        "location": {
            "address_line1": "123 main st",
            "address_line2": None,
            "address_line3": None,
            "foreign_province": None,
            "city_name": "Charlotte",
            "county_code": None,
            "county_name": "BUNCOMBE",
            "state_code": "NC",
            "state_name": "North Carolina",
            "zip5": "12204",
            "zip4": "5312",
            "foreign_postal_code": None,
            "country_name": "UNITED STATES",
            "location_country_code": "USA",
            "congressional_code": "90",
        },
    },
    "total_obligation": 1000.0,
    "base_and_all_options": 2000.0,
    "base_exercised_options": None,
    "place_of_performance": {
        "address_line1": None,
        "address_line2": None,
        "address_line3": None,
        "foreign_province": None,
        "city_name": "Austin",
        "county_code": None,
        "county_name": "Tripoli",
        "state_code": "TX",
        "state_name": "Texas",
        "zip5": "40221",
        "zip4": "2135",
        "foreign_postal_code": None,
        "country_name": "Pacific Delta Amazon",
        "location_country_code": "PDA",
        "congressional_code": "-0-",
    },
    "latest_transaction_contract_data": {
        "clinger_cohen_act_planning": None,
        "clinger_cohen_act_planning_description": "NO",
        "commercial_item_acquisition": "A",
        "commercial_item_acquisition_description": None,
        "commercial_item_test_program": None,
        "commercial_item_test_program_description": "NO",
        "consolidated_contract": None,
        "consolidated_contract_description": "NOT CONSOLIDATED",
        "construction_wage_rate": None,
        "construction_wage_rate_description": "NO",
        "cost_or_pricing_data": None,
        "cost_or_pricing_data_description": "NO",
        "dod_acquisition_program": "000",
        "dod_acquisition_program_description": None,
        "dod_claimant_program": None,
        "dod_claimant_program_description": "C9E",
        "domestic_or_foreign_entity": None,
        "domestic_or_foreign_entity_description": "U.S. OWNED BUSINESS",
        "evaluated_preference": None,
        "evaluated_preference_description": "NO PREFERENCE USED",
        "extent_competed": "D",
        "extent_competed_description": None,
        "fair_opportunity_limited": None,
        "fair_opportunity_limited_description": None,
        "fed_biz_opps": None,
        "fed_biz_opps_description": "YES",
        "foreign_funding": None,
        "foreign_funding_description": "NOT APPLICABLE",
        "idv_type_description": "IDC",
        "information_technology_commercial_item_category": None,
        "information_technology_commercial_item_category_description": "NOT IT PRODUCTS OR SERVICES",
        "interagency_contracting_authority": None,
        "interagency_contracting_authority_description": "NOT APPLICABLE",
        "labor_standards": None,
        "labor_standards_description": "NO",
        "major_program": None,
        "materials_supplies": None,
        "materials_supplies_description": "NO",
        "multi_year_contract": None,
        "multi_year_contract_description": "NO",
        "multiple_or_single_award_description": "MULTIPLE AWARD",
        "naics": "333911",
        "naics_description": "PUMP AND PUMPING EQUIPMENT MANUFACTURING",
        "national_interest_action": "H2020K",
        "national_interest_action_description": "HURRICANE KIRK",
        "number_of_offers_received": None,
        "other_than_full_and_open": None,
        "other_than_full_and_open_description": None,
        "price_evaluation_adjustment": None,
        "product_or_service_code": "4730",
        "product_or_service_description": None,
        "program_acronym": None,
        "purchase_card_as_payment_method": None,
        "purchase_card_as_payment_method_description": "NO",
        "referenced_idv_agency_iden": "168",
        "referenced_idv_agency_desc": "whatever",
        "sea_transportation": None,
        "sea_transportation_description": "NO",
        "small_business_competitive": False,
        "solicitation_identifier": None,
        "solicitation_procedures": "NP",
        "solicitation_procedures_description": None,
        "subcontracting_plan": "B",
        "subcontracting_plan_description": None,
        "type_of_contract_pricing": None,
        "type_of_contract_pricing_description": "FIRM FIXED PRICE",
        "type_of_idc_description": "INDEFINITE DELIVERY / INDEFINITE QUANTITY",
        "type_set_aside": None,
        "type_set_aside_description": None,
    },
    "subaward_count": 10,
    "total_subaward_amount": 12345.0,
    "executive_details": {
        "officers": [
            {"name": "Tom", "amount": 10000.00},
            {"name": "Stan Burger", "amount": 1234.00},
            {"name": None, "amount": None},
            {"name": None, "amount": None},
            {"name": None, "amount": None},
        ]
    },
    "date_signed": "2004-03-02",
    "naics_hierarchy": {
        "toptier_code": {"description": "Manufacturing", "code": "33"},
        "midtier_code": {"description": "Other General Purpose Machinery Manufacturing", "code": "3339"},
        "base_code": {"description": "PUMP AND PUMPING EQUIPMENT MANUFACTURING", "code": "333911"},
    },
    "psc_hierarchy": {
        "toptier_code": {},
        "midtier_code": {"description": "PIPE, TUBING, HOSE, AND FITTINGS", "code": "47"},
        "subtier_code": {},
        "base_code": {"description": "HOSE, PIPE, TUBE, LUBRICATION, AND RAILING FITTINGS", "code": "4730"},
    },
    "account_obligations_by_defc": [],
    "account_outlays_by_defc": [],
    "total_account_obligation": 0,
    "total_account_outlay": 0,
    "total_outlay": None,
}


recipient_without_id_and_name = {
    "recipient_hash": None,
    "recipient_name": None,
    "recipient_uei": None,
    "recipient_unique_id": None,
    "parent_recipient_hash": None,
    "parent_recipient_name": None,
    "parent_recipient_uei": None,
    "parent_recipient_unique_id": None,
    "business_categories": ["Small Business"],
    "location": {
        "address_line1": "123 main st",
        "address_line2": None,
        "address_line3": None,
        "foreign_province": None,
        "city_name": "Charlotte",
        "county_code": None,
        "county_name": "BUNCOMBE",
        "state_code": "NC",
        "state_name": "North Carolina",
        "zip5": "12204",
        "zip4": "5312",
        "foreign_postal_code": None,
        "country_name": "UNITED STATES",
        "location_country_code": "USA",
        "congressional_code": "90",
    },
}
