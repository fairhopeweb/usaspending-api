BROKER_SUBAWARDS_COLUMNS = {
    "created_at": {"delta": "TIMESTAMP", "postgres": "TIMESTAMP"},
    "updated_at": {"delta": "TIMESTAMP", "postgres": "TIMESTAMP"},
    "id": {"delta": "LONG NOT NULL", "postgres": "LONG NOT NULL"},
    # Prime Award Data
    "unique_award_key": {"delta": "STRING", "postgres": "TEXT"},
    "award_id": {"delta": "STRING", "postgres": "TEXT"},
    "parent_award_id": {"delta": "STRING", "postgres": "TEXT"},
    "award_amount": {"delta": "STRING", "postgres": "TEXT"},
    "action_date": {"delta": "STRING", "postgres": "TEXT"},
    "fy": {"delta": "STRING", "postgres": "TEXT"},
    "awarding_agency_code": {"delta": "STRING", "postgres": "TEXT"},
    "awarding_agency_name": {"delta": "STRING", "postgres": "TEXT"},
    "awarding_sub_tier_agency_c": {"delta": "STRING", "postgres": "TEXT"},
    "awarding_sub_tier_agency_n": {"delta": "STRING", "postgres": "TEXT"},
    "awarding_office_code": {"delta": "STRING", "postgres": "TEXT"},
    "awarding_office_name": {"delta": "STRING", "postgres": "TEXT"},
    "funding_agency_code": {"delta": "STRING", "postgres": "TEXT"},
    "funding_agency_name": {"delta": "STRING", "postgres": "TEXT"},
    "funding_sub_tier_agency_co": {"delta": "STRING", "postgres": "TEXT"},
    "funding_sub_tier_agency_na": {"delta": "STRING", "postgres": "TEXT"},
    "funding_office_code": {"delta": "STRING", "postgres": "TEXT"},
    "funding_office_name": {"delta": "STRING", "postgres": "TEXT"},
    "awardee_or_recipient_uniqu": {"delta": "STRING", "postgres": "TEXT"},
    "awardee_or_recipient_uei": {"delta": "STRING", "postgres": "TEXT"},
    "awardee_or_recipient_legal": {"delta": "STRING", "postgres": "TEXT"},
    "dba_name": {"delta": "STRING", "postgres": "TEXT"},
    "ultimate_parent_unique_ide": {"delta": "STRING", "postgres": "TEXT"},
    "ultimate_parent_uei": {"delta": "STRING", "postgres": "TEXT"},
    "ultimate_parent_legal_enti": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_country_code": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_country_name": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_address_line1": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_city_name": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_state_code": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_state_name": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_zip": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_county_code": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_county_name": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_congressional": {"delta": "STRING", "postgres": "TEXT"},
    "legal_entity_foreign_posta": {"delta": "STRING", "postgres": "TEXT"},
    "business_types": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perform_city_name": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perform_state_code": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perform_state_name": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_performance_zip": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_performance_county_code": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_performance_county_name": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perform_congressio": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perform_country_co": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perform_country_na": {"delta": "STRING", "postgres": "TEXT"},
    "award_description": {"delta": "STRING", "postgres": "TEXT"},
    "naics": {"delta": "STRING", "postgres": "TEXT"},
    "naics_description": {"delta": "STRING", "postgres": "TEXT"},
    "cfda_numbers": {"delta": "STRING", "postgres": "TEXT"},
    "cfda_titles": {"delta": "STRING", "postgres": "TEXT"},
    # Subaward Data
    "subaward_type": {"delta": "STRING", "postgres": "TEXT"},
    "subaward_report_year": {"delta": "STRING", "postgres": "TEXT"},
    "subaward_report_month": {"delta": "STRING", "postgres": "TEXT"},
    "subaward_number": {"delta": "STRING", "postgres": "TEXT"},
    "subaward_amount": {"delta": "STRING", "postgres": "TEXT"},
    "sub_action_date": {"delta": "STRING", "postgres": "TEXT"},
    "sub_awardee_or_recipient_uniqu": {"delta": "STRING", "postgres": "TEXT"},
    "sub_awardee_or_recipient_uei": {"delta": "STRING", "postgres": "TEXT"},
    "sub_awardee_or_recipient_legal": {"delta": "STRING", "postgres": "TEXT"},
    "sub_dba_name": {"delta": "STRING", "postgres": "TEXT"},
    "sub_ultimate_parent_unique_ide": {"delta": "STRING", "postgres": "TEXT"},
    "sub_ultimate_parent_uei": {"delta": "STRING", "postgres": "TEXT"},
    "sub_ultimate_parent_legal_enti": {"delta": "STRING", "postgres": "TEXT"},
    "sub_legal_entity_country_code": {"delta": "STRING", "postgres": "TEXT"},
    "sub_legal_entity_country_name": {"delta": "STRING", "postgres": "TEXT"},
    "sub_legal_entity_address_line1": {"delta": "STRING", "postgres": "TEXT"},
    "sub_legal_entity_city_name": {"delta": "STRING", "postgres": "TEXT"},
    "sub_legal_entity_state_code": {"delta": "STRING", "postgres": "TEXT"},
    "sub_legal_entity_state_name": {"delta": "STRING", "postgres": "TEXT"},
    "sub_legal_entity_zip": {"delta": "STRING", "postgres": "TEXT"},
    "sub_legal_entity_county_code": {"delta": "STRING", "postgres": "TEXT"},
    "sub_legal_entity_county_name": {"delta": "STRING", "postgres": "TEXT"},
    "sub_legal_entity_congressional": {"delta": "STRING", "postgres": "TEXT"},
    "sub_legal_entity_foreign_posta": {"delta": "STRING", "postgres": "TEXT"},
    "sub_business_types": {"delta": "STRING", "postgres": "TEXT"},
    "sub_place_of_perform_city_name": {"delta": "STRING", "postgres": "TEXT"},
    "sub_place_of_perform_state_code": {"delta": "STRING", "postgres": "TEXT"},
    "sub_place_of_perform_state_name": {"delta": "STRING", "postgres": "TEXT"},
    "sub_place_of_performance_zip": {"delta": "STRING", "postgres": "TEXT"},
    "sub_place_of_performance_county_code": {"delta": "STRING", "postgres": "TEXT"},
    "sub_place_of_performance_county_name": {"delta": "STRING", "postgres": "TEXT"},
    "sub_place_of_perform_congressio": {"delta": "STRING", "postgres": "TEXT"},
    "sub_place_of_perform_country_co": {"delta": "STRING", "postgres": "TEXT"},
    "sub_place_of_perform_country_na": {"delta": "STRING", "postgres": "TEXT"},
    "subaward_description": {"delta": "STRING", "postgres": "TEXT"},
    "sub_high_comp_officer1_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "sub_high_comp_officer1_amount": {"delta": "STRING", "postgres": "TEXT"},
    "sub_high_comp_officer2_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "sub_high_comp_officer2_amount": {"delta": "STRING", "postgres": "TEXT"},
    "sub_high_comp_officer3_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "sub_high_comp_officer3_amount": {"delta": "STRING", "postgres": "TEXT"},
    "sub_high_comp_officer4_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "sub_high_comp_officer4_amount": {"delta": "STRING", "postgres": "TEXT"},
    "sub_high_comp_officer5_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "sub_high_comp_officer5_amount": {"delta": "STRING", "postgres": "TEXT"},
    # Additional Prime Award Data
    "prime_id": {"delta": "INTEGER", "postgres": "INTEGER"},
    "internal_id": {"delta": "STRING", "postgres": "TEXT"},
    "date_submitted": {"delta": "STRING", "postgres": "TEXT"},
    "report_type": {"delta": "STRING", "postgres": "TEXT"},
    "transaction_type": {"delta": "STRING", "postgres": "TEXT"},
    "program_title": {"delta": "STRING", "postgres": "TEXT"},
    "contract_agency_code": {"delta": "STRING", "postgres": "TEXT"},
    "contract_idv_agency_code": {"delta": "STRING", "postgres": "TEXT"},
    "grant_funding_agency_id": {"delta": "STRING", "postgres": "TEXT"},
    "grant_funding_agency_name": {"delta": "STRING", "postgres": "TEXT"},
    "federal_agency_name": {"delta": "STRING", "postgres": "TEXT"},
    "treasury_symbol": {"delta": "STRING", "postgres": "TEXT"},
    "dunsplus4": {"delta": "STRING", "postgres": "TEXT"},
    "recovery_model_q1": {"delta": "STRING", "postgres": "TEXT"},
    "recovery_model_q2": {"delta": "STRING", "postgres": "TEXT"},
    "compensation_q1": {"delta": "STRING", "postgres": "TEXT"},
    "compensation_q2": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer1_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer1_amount": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer2_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer2_amount": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer3_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer3_amount": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer4_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer4_amount": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer5_full_na": {"delta": "STRING", "postgres": "TEXT"},
    "high_comp_officer5_amount": {"delta": "STRING", "postgres": "TEXT"},
    "place_of_perform_street": {"delta": "STRING", "postgres": "TEXT"},
    # Additional Subaward Data
    "sub_id": {"delta": "INTEGER", "postgres": "INTEGER"},
    "sub_parent_id": {"delta": "INTEGER", "postgres": "INTEGER"},
    "sub_federal_agency_id": {"delta": "STRING", "postgres": "TEXT"},
    "sub_federal_agency_name": {"delta": "STRING", "postgres": "TEXT"},
    "sub_funding_agency_id": {"delta": "STRING", "postgres": "TEXT"},
    "sub_funding_agency_name": {"delta": "STRING", "postgres": "TEXT"},
    "sub_funding_office_id": {"delta": "STRING", "postgres": "TEXT"},
    "sub_funding_office_name": {"delta": "STRING", "postgres": "TEXT"},
    "sub_naics": {"delta": "STRING", "postgres": "TEXT"},
    "sub_cfda_numbers": {"delta": "STRING", "postgres": "TEXT"},
    "sub_dunsplus4": {"delta": "STRING", "postgres": "TEXT"},
    "sub_recovery_subcontract_amt": {"delta": "STRING", "postgres": "TEXT"},
    "sub_recovery_model_q1": {"delta": "STRING", "postgres": "TEXT"},
    "sub_recovery_model_q2": {"delta": "STRING", "postgres": "TEXT"},
    "sub_compensation_q1": {"delta": "STRING", "postgres": "TEXT"},
    "sub_compensation_q2": {"delta": "STRING", "postgres": "TEXT"},
    "sub_place_of_perform_street": {"delta": "STRING", "postgres": "TEXT"},
}
BROKER_SUBAWARDS_DELTA_COLUMNS = {k: v["delta"] for k, v in BROKER_SUBAWARDS_COLUMNS.items()}
BROKER_SUBAWARDS_POSTGRES_COLUMNS = {k: v["postgres"] for k, v in BROKER_SUBAWARDS_COLUMNS.items()}

broker_subawards_sql_string = rf"""
    CREATE OR REPLACE TABLE {{DESTINATION_TABLE}} (
        {", ".join([f'{key} {val}' for key, val in BROKER_SUBAWARDS_DELTA_COLUMNS.items()])}
    )
    USING DELTA
    LOCATION 's3a://{{SPARK_S3_BUCKET}}/{{DELTA_LAKE_S3_PATH}}/{{DESTINATION_DATABASE}}/{{DESTINATION_TABLE}}'
"""

broker_subawards_load_sql_string = fr"""
    INSERT OVERWRITE {{DESTINATION_DATABASE}}.{{DESTINATION_TABLE}}
    (
        {", ".join([key for key in BROKER_SUBAWARDS_DELTA_COLUMNS])}
    )
    SELECT
        {", ".join([key for key in BROKER_SUBAWARDS_DELTA_COLUMNS])}
    FROM
        subaward
"""
