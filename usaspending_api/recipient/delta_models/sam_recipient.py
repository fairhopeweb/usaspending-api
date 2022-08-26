SAM_RECIPIENT_COLUMNS = {
    "awardee_or_recipient_uniqu": {"delta": "STRING", "postgres": "TEXT"},
    "legal_business_name": {"delta": "STRING", "postgres": "TEXT"},
    "ultimate_parent_unique_ide": {"delta": "STRING", "postgres": "TEXT"},
    "broker_duns_id": {"delta": "STRING", "postgres": "TEXT"},
    "update_date": {"delta": "DATE", "postgres": "DATE"},
    "address_line_1": {"delta": "STRING", "postgres": "TEXT"},
    "address_line_2": {"delta": "STRING", "postgres": "TEXT"},
    "city": {"delta": "STRING", "postgres": "TEXT"},
    "congressional_district": {"delta": "STRING", "postgres": "TEXT"},
    "country_code": {"delta": "STRING", "postgres": "TEXT"},
    "state": {"delta": "STRING", "postgres": "TEXT"},
    "zip": {"delta": "STRING", "postgres": "TEXT"},
    "zip4": {"delta": "STRING", "postgres": "TEXT"},
    "business_types_codes": {"delta": "ARRAY<STRING>", "postgres": "TEXT[]"},
    "dba_name": {"delta": "STRING", "postgres": "TEXT"},
    "entity_structure": {"delta": "STRING", "postgres": "TEXT"},
    "uei": {"delta": "STRING", "postgres": "TEXT"},
    "ultimate_parent_uei": {"delta": "STRING", "postgres": "TEXT"},
}

SAM_RECIPIENT_DELTA_COLUMNS = {k: v["delta"] for k, v in SAM_RECIPIENT_COLUMNS.items()}
SAM_RECIPIENT_POSTGRES_COLUMNS = {k: v["postgres"] for k, v in SAM_RECIPIENT_COLUMNS.items()}

sam_recipient_create_sql_string = rf"""
    CREATE OR REPLACE TABLE {{DESTINATION_TABLE}} (
        {", ".join([f'{key} {val}' for key, val in SAM_RECIPIENT_DELTA_COLUMNS.items()])}
    )
    USING DELTA
    LOCATION 's3a://{{SPARK_S3_BUCKET}}/{{DELTA_LAKE_S3_PATH}}/{{DESTINATION_DATABASE}}/{{DESTINATION_TABLE}}'
    """
sam_recipient_load_sql_string = [
    rf"""
CREATE OR REPLACE TEMPORARY VIEW source_data AS (
      SELECT
        ROW_NUMBER() OVER ( PARTITION BY broker_sam_recipient.award_or_recipient_uniqu
                            ORDER BY
                            awardee_or_recipient_uniqu ASC NULLS LAST,
                            activation_date DESC NULLS LAST
                            ) AS row_num,
        broker_sam_recipient.awardee_or_recipient_uniqu,
        broker_sam_recipient.legal_business_name,
        broker_sam_recipient.dba_name,
        broker_sam_recipient.ultimate_parent_unique_ide,
        broker_sam_recipient.ultimate_parent_legal_enti,
        broker_sam_recipient.address_line_1,
        broker_sam_recipient.address_line_2,
        broker_sam_recipient.city,
        broker_sam_recipient.state,
        broker_sam_recipient.zip,
        broker_sam_recipient.zip4,
        broker_sam_recipient.country_code,
        broker_sam_recipient.congressional_district,
        COALESCE(broker_sam_recipient.business_types_codes, text[]) AS business_types_codes,
        broker_sam_recipient.entity_structure,
        broker_sam_recipient.sam_recipient_id,
        COALESCE(broker_sam_recipient.activation_date, broker_sam_recipient.deactivation_date) as record_date,
        broker_sam_recipient.uei,
        broker_sam_recipient.ultimate_parent_uei
      FROM
        global_temp.sam_recipient as broker_sam_recipient
);""",
    rf"""
  INSERT OVERWRITE {{DESTINATION_DATABASE}}.{{DESTINATION_TABLE}}
    (
        {",".join([col for col in SAM_RECIPIENT_DELTA_COLUMNS])}
    )
  SELECT
    source_data.awardee_or_recipient_uniqu AS awardee_or_recipient_uniqu,
    source_data.legal_business_name AS legal_business_name,
    source_data.ultimate_parent_unique_ide AS ultimate_parent_unique_ide,
    source_data.ultimate_parent_legal_enti AS ultimate_parent_legal_enti,
    source_data.sam_recipient_id AS broker_duns_id,
    source_data.record_date AS update_date,
    source_data.address_line_1 AS address_line_1,
    source_data.address_line_2 AS address_line_2,
    source_data.city AS city,
    source_data.congressional_district AS congressional_district,
    source_data.country_code AS country_code,
    source_data.state AS state,
    source_data.zip AS zip,
    source_data.zip4 AS zip4,
    source_data.business_types_codes AS business_types_codes,
    source_data.dba_name as dba_name,
    source_data.entity_structure as entity_structure,
    source_data.uei AS uei,
    source_data.ultimate_parent_uei AS ultimate_parent_uei
  FROM
    source_data
  WHERE Source_data.row_num =1
);

""",
]
