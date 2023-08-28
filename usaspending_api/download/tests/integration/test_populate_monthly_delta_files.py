import zipfile
import datetime
import pytest
import os

from django.core.management import call_command
from os import listdir
from model_bakery import baker
from csv import reader

from usaspending_api.settings import HOST
from usaspending_api.awards.models import TransactionDelta
from usaspending_api.common.helpers.sql_helpers import get_database_dsn_string
from usaspending_api.download.v2.download_column_historical_lookups import query_paths


# Make sure UTC or test will fail later in the day
TODAY = datetime.datetime.strftime(datetime.datetime.utcnow(), "%Y%m%d")

@pytest.fixture
@pytest.mark.django_db(transaction=True)
def monthly_download_delta_data(db, monkeypatch):
    baker.make(
        "references.ToptierAgency", toptier_agency_id=1, toptier_code="001", name="Test_Agency", _fill_optional=True
    )
    baker.make("references.Agency", pk=1, toptier_agency_id=1, _fill_optional=True)
    baker.make(
        "references.ToptierAgency", toptier_agency_id=2, toptier_code="002", name="Test_Agency 2", _fill_optional=True
    )
    baker.make("references.Agency", pk=2, toptier_agency_id=2, _fill_optional=True)
    i = 1
    fiscal_year = 2020
    baker.make(
        "search.AwardSearch",
        award_id=i,
        generated_unique_award_id="CONT_AWD_1_0_0",
        is_fpds=True,
        type="B",
        type_description="Purchase Order",
        piid=f"piid{i}",
        awarding_agency_id=1,
        funding_agency_id=1,
        fiscal_year=fiscal_year,
    )
    baker.make("awards.FinancialAccountsByAwards", award_id=i)
    baker.make(
        "search.TransactionSearch",
        award_id=i,
        transaction_id=i,
        is_fpds=True,
        transaction_unique_id=i,
        usaspending_unique_transaction_id="",
        type="B",
        type_description="Purchase Order",
        period_of_performance_start_date=datetime.datetime(fiscal_year, 5, 7),
        period_of_performance_current_end_date=datetime.datetime(fiscal_year, 5, 7),
        action_date=datetime.datetime(fiscal_year, 5, 7),
        federal_action_obligation=100,
        modification_number="1",
        transaction_description="a description",
        last_modified_date=datetime.datetime(fiscal_year, 5, 7),
        award_certified_date=datetime.datetime(fiscal_year, 5, 7),
        etl_update_date=datetime.date.today(),
        create_date=datetime.datetime(fiscal_year, 5, 7),
        update_date=datetime.datetime(fiscal_year, 5, 7),
        fiscal_year=fiscal_year,
        awarding_agency_id=1,
        funding_agency_id=1,
        original_loan_subsidy_cost=100.0,
        face_value_loan_guarantee=100.0,
        funding_amount=100.0,
        non_federal_funding_amount=100.0,
        generated_unique_award_id="CONT_AWD_1_0_0",
        business_categories=[],
        detached_award_procurement_id=i,
        detached_award_proc_unique=f"test{i}",
        piid=f"piid{i}",
        agency_id=1,
        awarding_sub_tier_agency_c="001",
        awarding_subtier_agency_name="Test_Agency",
        awarding_agency_code="001",
        awarding_toptier_agency_name="Test_Agency",
        parent_award_id=f"000{i}",
        contract_award_type="B",
        contract_award_type_desc="Contract",
    )
    TransactionDelta.objects.update_or_create_transaction(i)

    monkeypatch.setenv("DOWNLOAD_DATABASE_URL", get_database_dsn_string())


@pytest.mark.django_db(transaction=True)
def test_all_agencies(monthly_download_delta_data, monkeypatch):
    call_command("populate_monthly_delta_files", "--debugging_skip_deleted", "--last_date=2020-12-31")
    file_list = listdir("csv_downloads")
    assert f"FY(All)_All_Contracts_Delta_{TODAY}.zip" in file_list
    os.remove(os.path.normpath(f"csv_downloads/FY(All)_All_Contracts_Delta_{TODAY}.zip"))


@pytest.mark.django_db(transaction=True)
def test_specific_agency(monthly_download_delta_data, monkeypatch):
    contract_data = [
        "",
        "1",
        "test1",
        "CONT_AWD_1_0_0",
        "piid1",
        "1",
        "",
        "",
        "",
        "0001",
        "",
        "100.00",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "2020-05-07",
        "2020",
        "2020-05-07",
        "2020-05-07",
        "",
        "",
        "",
        "001",
        "Test_Agency",
        "001",
        "Test_Agency",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "B",
        "Contract",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "a description",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        f"{HOST}/award/CONT_AWD_1_0_0/" if "localhost" in HOST else f"https://{HOST}/award/CONT_AWD_1_0_0/",
        "2020-05-07",
    ]
    call_command("populate_monthly_delta_files", "--agencies=1", "--debugging_skip_deleted", "--last_date=2020-12-31")
    file_list = listdir("csv_downloads")
    assert f"FY(All)_001_Contracts_Delta_{TODAY}.zip" in file_list
    with zipfile.ZipFile(
        os.path.normpath(f"csv_downloads/FY(All)_001_Contracts_Delta_{TODAY}.zip"), "r"
    ) as zip_ref:
        zip_ref.extractall("csv_downloads")
        assert f"FY(All)_001_Contracts_Delta_{TODAY}_1.csv" in listdir("csv_downloads")
    with open(
        os.path.normpath(f"csv_downloads/FY(All)_001_Contracts_Delta_{TODAY}_1.csv"), "r"
    ) as contract_file:
        csv_reader = reader(contract_file)
        row_count = 0
        for row in csv_reader:
            if row_count == 0:
                # 63 is the character limit for column names
                expected_row = [s[:63] for s in query_paths["transaction_search"]["d1"].keys()]
                # These cols are prepended during file processing
                expected_row = ["correction_delete_ind", "agency_id"] + expected_row
                assert row == expected_row
            else:
                assert row == contract_data
            row_count += 1
    assert row_count == 2
    os.remove(os.path.normpath(f"csv_downloads/FY(All)_001_Contracts_Delta_{TODAY}.zip"))
    os.remove(os.path.normpath(f"csv_downloads/FY(All)_001_Contracts_Delta_{TODAY}_1.csv"))


@pytest.mark.django_db(transaction=True)
def test_award_types(client, monthly_download_delta_data, monkeypatch):
    call_command(
        "populate_monthly_delta_files",
        "--agencies=1",
        "--award_types=assistance",
        "--debugging_skip_deleted",
        "--last_date=2020-12-31",
    )
    file_list = listdir("csv_downloads")
    assert f"FY(All)_001_Assistance_Delta_{TODAY}.zip" not in file_list

    baker.make(
        "search.AwardSearch",
        award_id=2,
        is_fpds=False,
        type="02",
        type_description="Block Grant",
        fain="fain2",
        awarding_agency_id=2,
        funding_agency_id=2,
        fiscal_year=2020,
    )
    baker.make(
        "search.TransactionSearch",
        award_id=2,
        transaction_id=2,
        is_fpds=False,
        transaction_unique_id=2,
        type="02",
        type_description="Block Grant",
        period_of_performance_start_date=datetime.datetime(2020, 5, 7),
        period_of_performance_current_end_date=datetime.datetime(2020, 5, 7),
        action_date=datetime.datetime(2020, 5, 7),
        last_modified_date=datetime.datetime(2020, 5, 7),
        award_certified_date=datetime.datetime(2020, 5, 7),
        etl_update_date=datetime.date.today(),
        create_date=datetime.datetime(2020, 5, 7),
        update_date=datetime.datetime(2020, 5, 7),
        fiscal_year=2020,
        awarding_agency_id=1,
        funding_agency_id=1,
        generated_unique_award_id=2,
        fain="fain2",
        awarding_agency_code="001",
        awarding_sub_tier_agency_c=1,
        awarding_toptier_agency_name="Test_Agency",
        awarding_subtier_agency_name="Test_Agency",
    )
    baker.make("awards.TransactionDelta", transaction_id=2, created_at=datetime.datetime.now())
    call_command(
        "populate_monthly_delta_files",
        "--agencies=1",
        "--award_types=assistance",
        "--debugging_skip_deleted",
        "--last_date=2020-12-31",
    )
    file_list = listdir("csv_downloads")
    assert f"FY(All)_001_Assistance_Delta_{TODAY}.zip" in file_list
    os.remove(os.path.normpath(f"csv_downloads/FY(All)_001_Assistance_Delta_{TODAY}.zip"))
