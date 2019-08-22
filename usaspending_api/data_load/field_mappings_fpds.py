from usaspending_api.data_load.derived_functions_fpds import calculate_usaspending_unique_transaction_id

transaction_fpds_columns = ["detached_award_procurement_id",
                           "detached_award_proc_unique",
                           "piid",
                           "agency_id",
                           "awarding_sub_tier_agency_c",
                           "awarding_sub_tier_agency_n",
                           "awarding_agency_code",
                           "awarding_agency_name",
                           "parent_award_id",
                           "award_modification_amendme",
                            "type_of_contract_pricing",
                            "type_of_contract_pric_desc",
                            "contract_award_type",
                            "contract_award_type_desc",
                            "naics",
                            "naics_description",
                            "awardee_or_recipient_uniqu",
                            "ultimate_parent_legal_enti",
                            "ultimate_parent_unique_ide",
                            "award_description",
                            "place_of_performance_zip4a",
                            "place_of_perform_city_name",
                            "place_of_perform_county_na",
                            "place_of_performance_congr",
                            "awardee_or_recipient_legal",
                            "legal_entity_city_name",
                            "legal_entity_state_code",
                            "legal_entity_state_descrip",
                            "legal_entity_zip4",
                            "legal_entity_congressional",
                            "legal_entity_address_line1",
                            "legal_entity_address_line2",
                            "legal_entity_address_line3",
                            "legal_entity_country_code",
                            "legal_entity_country_name",
                            "period_of_performance_star",
                            "period_of_performance_curr",
                            "period_of_perf_potential_e",
                            "ordering_period_end_date",
                            "action_date",
                            "action_type",
                            "action_type_description",
                            "federal_action_obligation",
                            "current_total_value_award",
                            "potential_total_value_awar",
                            "funding_sub_tier_agency_co",
                            "funding_sub_tier_agency_na",
                            "funding_office_code",
                            "funding_office_name",
                            "awarding_office_code",
                            "awarding_office_name",
                            "referenced_idv_agency_iden",
                            "referenced_idv_agency_desc",
                            "funding_agency_code",
                            "funding_agency_name",
                            "place_of_performance_locat",
                            "place_of_performance_state",
                            "place_of_perfor_state_desc",
                            "place_of_perform_country_c",
                            "place_of_perf_country_desc",
                            "idv_type",
                            "idv_type_description",
                            "referenced_idv_type",
                            "referenced_idv_type_desc",
                            "vendor_doing_as_business_n",
                            "vendor_phone_number",
                            "vendor_fax_number",
                            "multiple_or_single_award_i",
                            "multiple_or_single_aw_desc",
                            "referenced_mult_or_single",
                            "referenced_mult_or_si_desc",
                            "type_of_idc",
                            "type_of_idc_description",
                            "a_76_fair_act_action",
                            "a_76_fair_act_action_desc",
                            "dod_claimant_program_code",
                            "dod_claimant_prog_cod_desc",
                            "clinger_cohen_act_planning",
                            "clinger_cohen_act_pla_desc",
                            "commercial_item_acquisitio",
                            "commercial_item_acqui_desc",
                            "commercial_item_test_progr",
                            "commercial_item_test_desc",
                            "consolidated_contract",
                            "consolidated_contract_desc",
                            "contingency_humanitarian_o",
                            "contingency_humanitar_desc",
                            "contract_bundling",
                            "contract_bundling_descrip",
                            "contract_financing",
                            "contract_financing_descrip",
                            "contracting_officers_deter",
                            "contracting_officers_desc",
                            "cost_accounting_standards",
                            "cost_accounting_stand_desc",
                            "cost_or_pricing_data",
                            "cost_or_pricing_data_desc",
                            "country_of_product_or_serv",
                            "country_of_product_or_desc",
                            "construction_wage_rate_req",
                            "construction_wage_rat_desc",
                            "evaluated_preference",
                            "evaluated_preference_desc",
                            "extent_competed",
                            "extent_compete_description",
                            "fed_biz_opps",
                            "fed_biz_opps_description",
                            "foreign_funding",
                            "foreign_funding_desc",
                            "government_furnished_prope",
                            "government_furnished_desc",
                            "information_technology_com",
                            "information_technolog_desc",
                            "interagency_contracting_au",
                            "interagency_contract_desc",
                            "local_area_set_aside",
                            "local_area_set_aside_desc",
                            "major_program",
                            "purchase_card_as_payment_m",
                            "purchase_card_as_paym_desc",
                            "multi_year_contract",
                            "multi_year_contract_desc",
                            "national_interest_action",
                            "national_interest_desc",
                            "number_of_actions",
                            "number_of_offers_received",
                            "other_statutory_authority",
                            "performance_based_service",
                            "performance_based_se_desc",
                            "place_of_manufacture",
                            "place_of_manufacture_desc",
                            "price_evaluation_adjustmen",
                            "product_or_service_code",
                            "product_or_service_co_desc",
                            "program_acronym",
                            "other_than_full_and_open_c",
                            "other_than_full_and_o_desc",
                            "recovered_materials_sustai",
                            "recovered_materials_s_desc",
                            "research",
                            "research_description",
                            "sea_transportation",
                            "sea_transportation_desc",
                            "labor_standards",
                            "labor_standards_descrip",
                            "small_business_competitive",
                            "solicitation_identifier",
                            "solicitation_procedures",
                            "solicitation_procedur_desc",
                            "fair_opportunity_limited_s",
                            "fair_opportunity_limi_desc",
                            "subcontracting_plan",
                            "subcontracting_plan_desc",
                            "program_system_or_equipmen",
                            "program_system_or_equ_desc",
                            "type_set_aside",
                            "type_set_aside_description",
                            "epa_designated_product",
                            "epa_designated_produc_desc",
                            "materials_supplies_article",
                            "materials_supplies_descrip",
                            "transaction_number",
                            "sam_exception",
                            "sam_exception_description",
                            "city_local_government",
                            "county_local_government",
                            "inter_municipal_local_gove",
                            "local_government_owned",
                            "municipality_local_governm",
                            "school_district_local_gove",
                            "township_local_government",
                            "us_state_government",
                            "us_federal_government",
                            "federal_agency",
                            "federally_funded_research",
                            "us_tribal_government",
                            "foreign_government",
                            "community_developed_corpor",
                            "labor_surplus_area_firm",
                            "corporate_entity_not_tax_e",
                            "corporate_entity_tax_exemp",
                            "partnership_or_limited_lia",
                            "sole_proprietorship",
                            "small_agricultural_coopera",
                            "international_organization",
                            "us_government_entity",
                            "emerging_small_business",
                            "c8a_program_participant",
                            "sba_certified_8_a_joint_ve",
                            "dot_certified_disadvantage",
                            "self_certified_small_disad",
                            "historically_underutilized",
                            "small_disadvantaged_busine",
                            "the_ability_one_program",
                            "historically_black_college",
                            "c1862_land_grant_college",
                            "c1890_land_grant_college",
                            "c1994_land_grant_college",
                            "minority_institution",
                            "private_university_or_coll",
                            "school_of_forestry",
                            "state_controlled_instituti",
                            "tribal_college",
                            "veterinary_college",
                            "educational_institution",
                            "alaskan_native_servicing_i",
                            "community_development_corp",
                            "native_hawaiian_servicing",
                            "domestic_shelter",
                            "manufacturer_of_goods",
                            "hospital_flag",
                            "veterinary_hospital",
                            "hispanic_servicing_institu",
                            "foundation",
                            "woman_owned_business",
                            "minority_owned_business",
                            "women_owned_small_business",
                            "economically_disadvantaged",
                            "joint_venture_women_owned",
                            "joint_venture_economically",
                            "veteran_owned_business",
                            "service_disabled_veteran_o",
                            "contracts",
                            "grants",
                            "receives_contracts_and_gra",
                            "airport_authority",
                            "council_of_governments",
                            "housing_authorities_public",
                            "interstate_entity",
                            "planning_commission",
                            "port_authority",
                            "transit_authority",
                            "subchapter_s_corporation",
                            "limited_liability_corporat",
                            "foreign_owned_and_located",
                            "american_indian_owned_busi",
                            "alaskan_native_owned_corpo",
                            "indian_tribe_federally_rec",
                            "native_hawaiian_owned_busi",
                            "tribally_owned_business",
                            "asian_pacific_american_own",
                            "black_american_owned_busin",
                            "hispanic_american_owned_bu",
                            "native_american_owned_busi",
                            "subcontinent_asian_asian_i",
                            "other_minority_owned_busin",
                            "for_profit_organization",
                            "nonprofit_organization",
                            "other_not_for_profit_organ",
                            "us_local_government",
                            "referenced_idv_modificatio",
                            "undefinitized_action",
                            "undefinitized_action_desc",
                            "domestic_or_foreign_entity",
                            "domestic_or_foreign_e_desc",
                            "pulled_from",
                            "last_modified",
                            "annual_revenue",
                            "division_name",
                            "division_number_or_office",
                            "number_of_employees",
                            "vendor_alternate_name",
                            "vendor_alternate_site_code",
                            "vendor_enabled",
                            "vendor_legal_org_name",
                            "vendor_location_disabled_f",
                            "vendor_site_code",
                            "initial_report_date",
                            "base_and_all_options_value",
                            "base_exercised_options_val",
                            "total_obligated_amount",
                            "place_of_perform_country_n",
                            "place_of_perform_state_nam",
                            "referenced_idv_agency_name",
                            "award_or_idv_flag",
                            "legal_entity_county_code",
                            "legal_entity_county_name",
                            "legal_entity_zip5",
                            "legal_entity_zip_last4",
                            "place_of_perform_county_co",
                            "place_of_performance_zip5",
                            "place_of_perform_zip_last4",
                            "cage_code",
                            "inherently_government_func",
                            "organizational_type",
                            "inherently_government_desc",
                            "unique_award_key",
                            "high_comp_officer1_amount",
                            "high_comp_officer1_full_na",
                            "high_comp_officer2_amount",
                            "high_comp_officer2_full_na",
                            "high_comp_officer3_amount",
                            "high_comp_officer3_full_na",
                            "high_comp_officer4_amount",
                            "high_comp_officer4_full_na",
                            "high_comp_officer5_amount",
                            "high_comp_officer5_full_na",
                            "award_modification_amendme"]

# broker column name -> usaspending column name
transaction_normalized_columns = {"federal_action_obligation": "federal_action_obligation",
                                  "action_date": "action_date",
                                  "action_type": "action_type",
                                  "action_type_description": "action_type_description",
                                  "period_of_performance_star": "period_of_performance_start_date",
                                  "period_of_performance_curr": "period_of_performance_current_end_date",
                                  "detached_award_proc_unique": "detached_award_proc_unique",
                                  "award_description": "description",
                                  "last_modified": "last_modified_date",
                                  "federal_action_obligation": "federal_action_obligation",
                                  "award_modification_amendme": "modification_number",
                                  "detached_award_proc_unique": "transaction_unique_id",
                                  "unique_award_key": "unique_award_key",
                                  "last_modified": "last_modified_date"}

# usaspending column name -> derivation function
transaction_normalized_functions = {"usaspending_unique_transaction_id": lambda broker: None,
                                    "original_loan_subsidy_cost": lambda broker: None,
                                    "face_value_loan_guarantee": lambda broker: None,
                                    "non_federal_funding_amount": lambda broker: None}
