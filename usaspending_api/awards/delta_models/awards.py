awards_sql_string = r"""
    CREATE OR REPLACE TABLE {DESTINATION_TABLE} (
        id LONG NOT NULL,
        generated_unique_award_id STRING NOT NULL,
        is_fpds BOOLEAN NOT NULL,
        transaction_unique_id STRING NOT NULL,
        data_source STRING,
        type STRING,
        type_description STRING,
        piid STRING,
        parent_award_piid STRING,
        fain STRING,
        uri STRING,
        total_obligation NUMERIC(23,2),
        base_and_all_options_value NUMERIC(23,2),
        total_subsidy_cost NUMERIC(23,2),
        date_signed DATE,
        description STRING,
        period_of_performance_start_date DATE,
        period_of_performance_current_end_date DATE,
        last_modified_date DATE,
        certified_date DATE,
        create_date TIMESTAMP,
        update_date TIMESTAMP,
        total_subaward_amount NUMERIC(23,2),
        subaward_count INTEGER NOT NULL,
        awarding_agency_id INTEGER,
        funding_agency_id INTEGER,
        latest_transaction_id LONG,
        category STRING,
        fiscal_year INTEGER,
        total_loan_value NUMERIC(23,2),
        total_funding_amount NUMERIC(23,2),
        non_federal_funding_amount NUMERIC(23,2),
        base_exercised_options_val NUMERIC(23,2),
        fpds_agency_id STRING,
        fpds_parent_agency_id STRING,
        officer_1_amount NUMERIC(23,2),
        officer_1_name STRING,
        officer_2_amount NUMERIC(23,2),
        officer_2_name STRING,
        officer_3_amount NUMERIC(23,2),
        officer_3_name STRING,
        officer_4_amount NUMERIC(23,2),
        officer_4_name STRING,
        officer_5_amount NUMERIC(23,2),
        officer_5_name STRING,
        earliest_transaction_id LONG
    )
    USING DELTA
    LOCATION 's3a://{SPARK_S3_BUCKET}/{DELTA_LAKE_S3_PATH}/{DESTINATION_DATABASE}/{DESTINATION_TABLE}'
"""
