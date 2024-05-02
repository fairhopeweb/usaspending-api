import json
import pytest

from model_bakery import baker
from time import perf_counter
from rest_framework import status

from usaspending_api.search.tests.data.utilities import setup_elasticsearch_test

ENDPOINT = "/api/v2/search/spending_by_transaction_grouped/"


@pytest.fixture
def transaction_data():
    baker.make(
        "search.TransactionSearch",
        transaction_id=1,
        award_id=1,
        action_date="2010-10-01",
        is_fpds=True,
        type="A",
        transaction_description="award 1",
        federal_action_obligation=35.01,
        recipient_location_zip5="abcde",
        piid="IND12PB00323",
        recipient_uei="testuei",
        parent_uei="test_parent_uei",
    )
    baker.make(
        "search.TransactionSearch",
        transaction_id=2,
        award_id=1,
        action_date="2011-10-01",
        is_fpds=True,
        type="A",
        transaction_description="award 1",
        federal_action_obligation=100,
        recipient_location_zip5="abcde",
        piid="IND12PB00323",
        recipient_uei="testuei",
        parent_uei="test_parent_uei",
    )
    baker.make("search.AwardSearch", award_id=1, latest_transaction_id=2, is_fpds=True, type="A", piid="IND12PB00323")

    baker.make(
        "search.TransactionSearch",
        transaction_id=3,
        award_id=2,
        action_date="2012-10-01",
        is_fpds=True,
        type="A",
        transaction_description="award 2",
        federal_action_obligation=35.01,
        recipient_location_zip5="abcde",
        piid="BOI1243L98AS",
        recipient_uei="testuei",
        parent_uei="test_parent_uei",
    )
    baker.make(
        "search.TransactionSearch",
        transaction_id=4,
        award_id=2,
        action_date="2013-10-01",
        is_fpds=True,
        type="A",
        transaction_description="award 2",
        federal_action_obligation=30,
        recipient_location_zip5="abcde",
        piid="BOI1243L98AS",
        recipient_uei="testuei",
        parent_uei="test_parent_uei",
    )
    baker.make("search.AwardSearch", award_id=2, latest_transaction_id=4, is_fpds=True, type="A", piid="BOI1243L98AS")


@pytest.mark.django_db
def test_spending_by_transaction_grouped_success(
    client, monkeypatch, transaction_data, elasticsearch_transaction_index
):
    setup_elasticsearch_test(monkeypatch, elasticsearch_transaction_index)

    resp = client.post(
        ENDPOINT,
        content_type="application/json",
        data=json.dumps({"filters": {"keywords": ["award 1"], "award_type_codes": ["A"]}}),
    )

    resp_results = resp.data.get("results", {})
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp_results) == 1
    assert resp_results[0]["Prime Award ID"] == "IND12PB00323"
    assert resp_results[0]["Matching Transaction Count"] == 2
    assert resp_results[0]["Matching Transaction Obligation"] == 135.01
    assert len(resp_results[0]["children"]) == 2
    assert resp_results[0][0]["Transaction Amount"] == 35.01
    assert resp_results[0][1]["Transaction Amount"] == 100

    resp = client.post(
        ENDPOINT,
        content_type="application/json",
        data=json.dumps({"filters": {"keywords": ["award 1"], "award_type_codes": ["B"]}}),
    )

    resp_results = resp.data.get("results", {})
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp_results) == 0

    # Test that `keyword` can be used
    resp = client.post(
        ENDPOINT,
        content_type="application/json",
        data=json.dumps({"filters": {"keyword": "award 1", "award_type_codes": ["A"]}}),
    )

    resp_results = resp.data.get("results", {})
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp_results) == 1
    assert resp_results[0]["Prime Award ID"] == "IND12PB00323"
    assert resp_results[0]["Matching Transaction Count"] == 2
    assert resp_results[0]["Matching Transaction Obligation"] == 135.01
    assert len(resp_results[0]["children"]) == 2
    assert resp_results[0][0]["Transaction Amount"] == 35.01
    assert resp_results[0][1]["Transaction Amount"] == 100

    # Test required filters
    resp = client.post(
        ENDPOINT,
        content_type="application/json",
        data=json.dumps({"filters": {"award_type_codes": ["A"]}}),
    )
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    resp = client.post(
        ENDPOINT,
        content_type="application/json",
        data=json.dumps({"filters": {"keywords": ["award 1"]}}),
    )
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Test multiple prime awards in results
    resp = client.post(
        ENDPOINT,
        content_type="application/json",
        data=json.dumps({"filters": {"keywords": ["award 1", "award 2"], "award_type_codes": ["A"]}}),
    )

    resp_results = resp.data.get("results", {})
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp_results) == 2
    assert resp_results[0]["Prime Award ID"] == "IND12PB00323"
    assert resp_results[0]["Matching Transaction Count"] == 2
    assert resp_results[0]["Matching Transaction Obligation"] == 135.01
    assert len(resp_results[0]["children"]) == 2
    assert resp_results[0][0]["Transaction Amount"] == 35.01
    assert resp_results[0][1]["Transaction Amount"] == 100
    assert resp_results[1]["Prime Award ID"] == "BOI1243L98AS"
    assert resp_results[1]["Matching Transaction Count"] == 2
    assert resp_results[1]["Matching Transaction Obligation"] == 65.01
    assert len(resp_results[1]["children"]) == 2
    assert resp_results[1][0]["Transaction Amount"] == 30
    assert resp_results[1][1]["Transaction Amount"] == 35.01


@pytest.mark.django_db
def test_spending_by_transaction_grouped_sorting(
    client, monkeypatch, transaction_data, elasticsearch_transaction_index
):
    setup_elasticsearch_test(monkeypatch, elasticsearch_transaction_index)

    # Test sort order
    resp = client.post(
        ENDPOINT,
        content_type="application/json",
        data=json.dumps({"filters": {"keywords": ["award 1", "award 2"], "award_type_codes": ["A"]}, "order": "asc"}),
    )

    resp_results = resp.data.get("results", {})
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp_results) == 2
    assert resp_results[0]["Prime Award ID"] == "BOI1243L98AS"
    assert resp_results[0]["Matching Transaction Count"] == 2
    assert resp_results[0]["Matching Transaction Obligation"] == 65.01
    assert len(resp_results[0]["children"]) == 2
    assert resp_results[0][0]["Transaction Amount"] == 30
    assert resp_results[0][1]["Transaction Amount"] == 35.01
    assert resp_results[1]["Prime Award ID"] == "IND12PB00323"
    assert resp_results[1]["Matching Transaction Count"] == 2
    assert resp_results[1]["Matching Transaction Obligation"] == 135.01
    assert len(resp_results[1]["children"]) == 2
    assert resp_results[1][0]["Transaction Amount"] == 35.01
    assert resp_results[1][1]["Transaction Amount"] == 100

    # Test sort field
    resp = client.post(
        ENDPOINT,
        content_type="application/json",
        data=json.dumps(
            {"filters": {"keywords": ["award 1", "award 2"], "award_type_codes": ["A"]}, "sort": "Prime Award ID"}
        ),
    )

    resp_results = resp.data.get("results", {})
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp_results) == 2
    assert resp_results[0]["Prime Award ID"] == "IND12PB00323"
    assert resp_results[0]["Matching Transaction Count"] == 2
    assert resp_results[0]["Matching Transaction Obligation"] == 135.01
    assert len(resp_results[0]["children"]) == 2
    assert resp_results[0][0]["Transaction Amount"] == 35.01
    assert resp_results[0][1]["Transaction Amount"] == 100
    assert resp_results[1]["Prime Award ID"] == "BOI1243L98AS"
    assert resp_results[1]["Matching Transaction Count"] == 2
    assert resp_results[1]["Matching Transaction Obligation"] == 65.01
    assert len(resp_results[1]["children"]) == 2
    assert resp_results[1][0]["Transaction Amount"] == 30
    assert resp_results[1][1]["Transaction Amount"] == 35.01
