PUBLISHED_FABS_COLUMNS = {
    "published_fabs_id": {"delta": "INTEGER", "postgres": "INTEGER"},
    "afa_generated_unique": {"delta": "STRING", "postgres": "TEXT"},
    "action_date": {"delta": "STRING", "postgres": "TEXT"},
    "action_type": {"delta": "STRING", "postgres": "TEXT"},
    "action_type_description": {"delta": "STRING", "postgres": "TEXT"},
    "assistance_type": {"delta": "STRING", "postgres": "TEXT"},
    "assistance_type_desc": {"delta": "STRING", "postgres": "TEXT"},
    "award_description": {"delta": "STRING", "postgres": "TEXT"},
    "award_modification_amendme": {"delta": "STRING", "postgres": "TEXT"},
    "awardee_or_recipient_legal": {"delta": "STRING", "postgres": "TEXT"},
    "awardee_or_recipient_uniqu": {"delta": "STRING", "postgres": "TEXT"},
    "awarding_agency_code": {"delta": "STRING", "postgres": "TEXT"},
    "awarding_agency_name": {"delta": "STRING", "postgres": "TEXT"},
    "awarding_office_code": {"delta": "STRING", "postgres": "TEXT"},
    "awarding_office_name": {"delta": "STRING", "postgres": "TEXT"},
    "awarding_sub_tier_agency_c": {"delta": "STRING", "postgres": "TEXT"},
    "awarding_sub_tier_agency_n": {"delta": "STRING", "postgres": "TEXT"},
    "business_categories": {"delta": "ARRAY<STRING>", "postgres": "ARRAYTEXT[]"},
    "business_funds_ind_desc": {"delta": "STRING", "postgres": "TEXT"},
    "business_funds_indicator": {"delta": "STRING", "postgres": "TEXT"},
    "business_types": {"delta": "STRING", "postgres": "TEXT"},
    "business_types_desc": {"delta": "STRING", "postgres": "TEXT"},
    "cfda_number": {"delta": "STRING", "postgres": "TEXT"},
    "cfda_title": {"delta": "STRING", "postgres": "TEXT"},
    "correction_delete_ind_desc": {"delta": "STRING", "postgres": "TEXT"},
    "correction_delete_indicatr": {"delta": "STRING", "postgres": "TEXT"},
    "created_at": {"delta": "TIMESTAMP", "postgres": "TIMESTAMP"},
    "face_value_loan_guarantee": {"delta": "NUMERIC", "postgres": "NUMERIC"},
    "fain": {"delta": "STRING", "postgres": "TEXT"},
    "federal_action_obligation": {"delta": "NUMERIC", "postgres": "NUMERIC"},
    "fiscal_year_and_quarter_co": {"delta": "STRING", "postgres": "TEXT"},
    "funding_agency_code": {"delta": "STRING", "postgres": "TEXT"},
    "funding_agency_name": {"delta": "STRING", "postgres": "TEXT"},
    "funding_office_code": {"delta": "STRING", "postgres": "TEXT"},
    "funding_office_name": {"delta": "STRING", "postgres": "TEXT"},
    "funding_opportunity_goals": {"delta": "STRING", "postgres": "TEXT"},
    "funding_opportunity_number": {"delta": "STRING", "postgres": "TEXT"},
    "funding_sub_tier_agency_co": {"delta": "STRING", "postgres": "TEXT"},
    "funding_sub_tier_agency_na": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer1_amount": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer1_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer2_amount": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer2_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer3_amount": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer3_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer4_amount": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer4_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer5_amount": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer5_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "indirect_federal_sharing": {"delta": "NUMERIC", "postgres": "NUMERIC"},
    "is_active": {"delta": "BOOLEAN", "postgres": "BOOLEAN"},
    "is_historical": {"delta": "BOOLEAN", "postgres": "BOOLEAN"},
    "legal_entity_address_line1": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_address_line2": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_address_line3": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_city_code": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_city_name": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_congressional": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_country_code": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_country_name": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_county_code": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_county_name": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_foreign_city": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_foreign_descr": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_foreign_posta": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_foreign_provi": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_state_code": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_state_name": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_zip5": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_zip_last4": {"delta": "STRING", "postgres": "TEXT"},
    "modified_at": {"delta": "TIMESTAMP", "postgres": "TIMESTAMP"},
    "non_federal_funding_amount": {"delta": "NUMERIC", "postgres": "NUMERIC"},
    "original_loan_subsidy_cost": {"delta": "NUMERIC", "postgres": "NUMERIC"},
    "period_of_performance_curr": {"delta": "STRING", "postgres": "TEXT"},
    "period_of_performance_star": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perfor_state_code": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perform_country_c": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perform_country_n": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perform_county_co": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perform_county_na": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perform_state_nam": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perform_zip_last4": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_performance_city": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_performance_code": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_performance_congr": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_performance_forei": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_performance_zip4a": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_performance_zip5": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_performance_scope": {"delta": "STRING", "postgres": "TEXT"},
    "record_type": {"delta": "INTEGER", "postgres": "INTEGER"},
    "record_type_description": {"delta": "STRING", "postgres": "TEXT"},
    "sai_number": {"delta": "STRING", "postgres": "TEXT"},
    "submission_id": {"delta": "NUMERIC", "postgres": "NUMERIC"},
    "total_funding_amount": {"delta": "STRING", "postgres": "TEXT"},
    "uei": {"delta": "STRING", "postgres": "TEXT"},
    "ultimate_parent_legal_enti": {"delta": "STRING", "postgres": "TEXT"},
    "ultimate_parent_uei": {"delta": "STRING", "postgres": "TEXT"},
    "ultimate_parent_unique_ide": {"delta": "STRING", "postgres": "TEXT"},
    "unique_award_key": {"delta": "STRING", "postgres": "TEXT"},
    "updated_at": {"delta": "TIMESTAMP", "postgres": "TIMESTAMP"},
    "uri": {"delta": "STRING", "postgres": "TEXT"},
}
PUBLISHED_FABS_DELTA_COLUMNS = {k: v["delta"] for k, v in PUBLISHED_FABS_COLUMNS.items()}
PUBLISHED_FABS_POSTGRES_COLUMNS = {k: v["postgres"] for k, v in PUBLISHED_FABS_COLUMNS.items()}

published_fabs_create_sql_string = fr"""
    CREATE OR REPLACE TABLE {{DESTINATION_TABLE}} (
        {", ".join([f'{key} {val}' for key, val in PUBLISHED_FABS_DELTA_COLUMNS.items()])}
    )
    USING DELTA
    LOCATION 's3a://{{SPARK_S3_BUCKET}}/{{DELTA_LAKE_S3_PATH}}/{{DESTINATION_DATABASE}}/{{DESTINATION_TABLE}}'
"""
