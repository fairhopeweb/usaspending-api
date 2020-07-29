import json

from datetime import datetime, timezone, date
from django.db.models import Max, Q, F, Value, Case, When, Sum, Count
from django.db.models.functions import Coalesce, Concat
from django.http import HttpRequest
from django.utils.functional import cached_property
from django_cte import With
from functools import lru_cache
from rest_framework.views import APIView
from typing import List

from usaspending_api.awards.models.financial_accounts_by_awards import FinancialAccountsByAwards
from usaspending_api.awards.v2.lookups.lookups import award_type_mapping, loan_type_mapping, assistance_type_mapping
from usaspending_api.common.containers import Bunch
from usaspending_api.common.data_classes import Pagination
from usaspending_api.common.helpers.fiscal_year_helpers import generate_fiscal_year_and_month
from usaspending_api.common.validator import customize_pagination_with_sort_columns, TinyShield
from usaspending_api.references.models import DisasterEmergencyFundCode
from usaspending_api.references.models.gtas_sf133_balances import GTASSF133Balances
from usaspending_api.submissions.helpers import get_last_closed_submission_date
from usaspending_api.submissions.models import DABSSubmissionWindowSchedule

COVID_19_GROUP_NAME = "covid_19"

REPORTING_PERIOD_MIN_DATE = date(2020, 4, 1)
REPORTING_PERIOD_MIN_YEAR, REPORTING_PERIOD_MIN_MONTH = generate_fiscal_year_and_month(REPORTING_PERIOD_MIN_DATE)


def latest_gtas_of_each_year_queryset():
    q = Q()
    for sub in final_submissions_for_all_fy():
        if not sub.is_quarter:
            q |= Q(fiscal_year=sub.fiscal_year) & Q(fiscal_period=sub.fiscal_period)
    if not q:
        return GTASSF133Balances.objects.none()
    return GTASSF133Balances.objects.filter(q)


def latest_faba_of_each_year_queryset() -> FinancialAccountsByAwards:
    q = filter_by_latest_closed_periods()
    if not q:
        return FinancialAccountsByAwards.objects.none()
    return FinancialAccountsByAwards.objects.filter(q)


def filter_by_latest_closed_periods() -> Q:
    """Return Django Q for all latest closed submissions (quarterly and monthly)"""
    q = Q()
    for sub in final_submissions_for_all_fy():
        q |= (
            Q(submission__reporting_fiscal_year=sub.fiscal_year)
            & Q(submission__quarter_format_flag=sub.is_quarter)
            & Q(submission__reporting_fiscal_period=sub.fiscal_period)
        )
    return q


def filter_by_defc_closed_periods() -> Q:
    """
        These filters should only be used when looking at submission data
        that includes DEF Codes, which only started appearing in submission
        for FY2020 P07 (Apr 1, 2020) and after
    """
    q = Q()
    for sub in final_submissions_for_all_fy():
        if (
            sub.fiscal_year == REPORTING_PERIOD_MIN_YEAR and sub.fiscal_period >= REPORTING_PERIOD_MIN_MONTH
        ) or sub.fiscal_year > REPORTING_PERIOD_MIN_YEAR:
            q |= (
                Q(submission__reporting_fiscal_year=sub.fiscal_year)
                & Q(submission__quarter_format_flag=sub.is_quarter)
                & Q(submission__reporting_fiscal_period__lte=sub.fiscal_period)
            )
    if not q:
        # Edgecase not expected in production. If there are no DABS between
        # FY2020 P07 (Apr 1, 2020) and now() then ensure nothing is returned
        q = Q(pk__isnull=True)
    return q & Q(submission__reporting_period_start__gte=str(REPORTING_PERIOD_MIN_DATE))


@lru_cache(maxsize=1)
def final_submissions_for_all_fy() -> List[tuple]:
    """
        Returns a list the latest monthly and quarterly submission for each
        fiscal year IF it is "closed" aka ready for display on USAspending.gov
    """
    return (
        DABSSubmissionWindowSchedule.objects.filter(submission_reveal_date__lte=datetime.now(timezone.utc))
        .values("submission_fiscal_year", "is_quarter")
        .annotate(fiscal_year=F("submission_fiscal_year"), fiscal_period=Max("submission_fiscal_month"))
        .values_list("fiscal_year", "is_quarter", "fiscal_period", named=True)
    )


class DisasterBase(APIView):
    required_filters = ["def_codes"]

    @classmethod
    def requests_award_type_codes(cls, request: HttpRequest) -> bool:
        """Return True if an endpoint was requested with filter.award_type_codes"""

        # NOTE: The point at which this is used in the request life cycle, it has not been post-processed to include
        # a POST or data attribute. Must get payload from body
        if request and request.body:
            body_json = json.loads(request.body)
            if "filter" in body_json and "award_type_codes" in body_json["filter"]:
                return True
        return False

    @classmethod
    def requests_award_spending_type(cls, request: HttpRequest) -> bool:
        """Return True if an endpoint was requested with spending_type = award"""

        # NOTE: The point at which this is used in the request life cycle, it has not been post-processed to include
        # a POST or data attribute. Must get payload from body
        if request and request.body:
            body_json = json.loads(request.body)
            if body_json.get("spending_type", "") == "award":
                return True
        return False

    @cached_property
    def filters(self):
        all_def_codes = sorted(DisasterEmergencyFundCode.objects.values_list("code", flat=True))
        object_keys_lookup = {
            "def_codes": {
                "key": "filter|def_codes",
                "name": "def_codes",
                "type": "array",
                "array_type": "enum",
                "enum_values": all_def_codes,
                "allow_nulls": False,
                "optional": False,
            },
            "query": {
                "key": "filter|query",
                "name": "query",
                "type": "text",
                "text_type": "search",
                "allow_nulls": True,
                "optional": True,
            },
            "award_type_codes": {
                "key": "filter|award_type_codes",
                "name": "award_type_codes",
                "type": "array",
                "array_type": "enum",
                "enum_values": sorted(award_type_mapping.keys()),
                "allow_nulls": True,
                "optional": True,
            },
            "_loan_award_type_codes": {
                "key": "filter|award_type_codes",
                "name": "award_type_codes",
                "type": "array",
                "array_type": "enum",
                "enum_values": sorted(loan_type_mapping.keys()),
                "allow_nulls": True,
                "optional": True,
                "default": list(loan_type_mapping.keys()),
            },
            "_assistance_award_type_codes": {
                "key": "filter|award_type_codes",
                "name": "award_type_codes",
                "type": "array",
                "array_type": "enum",
                "enum_values": sorted(assistance_type_mapping.keys()),
                "allow_nulls": True,
                "optional": True,
                "default": list(assistance_type_mapping.keys()),
            },
        }
        model = [object_keys_lookup[key] for key in self.required_filters]
        json_request = TinyShield(model).block(self.request.data)
        return json_request["filter"]

    @property
    def def_codes(self):
        return self.filters["def_codes"]

    @cached_property
    def final_period_submission_query_filters(self):
        return filter_by_latest_closed_periods()

    @cached_property
    def latest_reporting_period(self):
        return get_last_closed_submission_date(False)

    @cached_property
    def all_closed_defc_submissions(self):
        return filter_by_defc_closed_periods()

    @property
    def is_in_provided_def_codes(self):
        return Q(disaster_emergency_fund__code__in=self.def_codes)

    @property
    def is_non_zero_total_spending(self):
        return Q(
            Q(obligations_incurred_by_program_object_class_cpe__gt=0)
            | Q(obligations_incurred_by_program_object_class_cpe__lt=0)
            | Q(gross_outlay_amount_by_program_object_class_cpe__gt=0)
            | Q(gross_outlay_amount_by_program_object_class_cpe__lt=0)
        )

    @property
    def is_provided_award_type(self):
        return Q(type__in=self.filters.get("award_type_codes"))

    @property
    def has_award_of_provided_type(self):
        if self.filters.get("award_type_codes"):
            return Q(award__type__in=self.filters.get("award_type_codes")) & Q(award__isnull=False)
        else:
            return ~Q(pk=None)  # always true; if types are not provided we don't check types

    @property
    def has_award_of_classification(self):
        if self.filters.get("award_type"):
            # Simple check: if "procurement" then piid cannot be null, otherwise piid must be null
            return Q(piid__isnull=bool(self.filters["award_type"] == "assistance"))
        else:
            return ~Q(pk=None)  # always true; if types are not provided we don't check types

    def construct_loan_queryset(self, faba_grouping_column, base_model, base_model_column):
        grouping_key = F(faba_grouping_column) if isinstance(faba_grouping_column, str) else faba_grouping_column

        base_values = With(
            FinancialAccountsByAwards.objects.filter(
                Q(award__type__in=loan_type_mapping), self.all_closed_defc_submissions, self.is_in_provided_def_codes,
            )
            .annotate(
                grouping_key=grouping_key,
                total_loan_value=F("award__total_loan_value"),
                reporting_fiscal_year=F("submission__reporting_fiscal_year"),
                reporting_fiscal_period=F("submission__reporting_fiscal_period"),
                quarter_format_flag=F("submission__quarter_format_flag"),
            )
            .filter(grouping_key__isnull=False)
            .values(
                "grouping_key",
                "financial_accounts_by_awards_id",
                "award_id",
                "transaction_obligated_amount",
                "gross_outlay_amount_by_award_cpe",
                "reporting_fiscal_year",
                "reporting_fiscal_period",
                "quarter_format_flag",
                "total_loan_value",
            ),
            "base_values",
        )

        q = Q()
        for sub in final_submissions_for_all_fy():
            q |= (
                Q(reporting_fiscal_year=sub.fiscal_year)
                & Q(quarter_format_flag=sub.is_quarter)
                & Q(reporting_fiscal_period=sub.fiscal_period)
            )

        aggregate_faba = With(
            base_values.queryset()
            .values("grouping_key")
            .annotate(
                obligation=Coalesce(Sum("transaction_obligated_amount"), 0),
                outlay=Coalesce(Sum(Case(When(q, then=F("gross_outlay_amount_by_award_cpe")), default=Value(0),)), 0,),
            )
            .values("grouping_key", "obligation", "outlay"),
            "aggregate_faba",
        )

        distinct_awards = With(
            base_values.queryset().values("grouping_key", "award_id", "total_loan_value").distinct(), "distinct_awards",
        )

        aggregate_awards = With(
            distinct_awards.queryset()
            .values("grouping_key")
            .annotate(award_count=Count("award_id"), face_value_of_loan=Coalesce(Sum("total_loan_value"), 0))
            .values("grouping_key", "award_count", "face_value_of_loan"),
            "aggregate_awards",
        )

        return Bunch(
            award_count_column=aggregate_awards.col.award_count,
            obligation_column=aggregate_faba.col.obligation,
            outlay_column=aggregate_faba.col.outlay,
            face_value_of_loan_column=aggregate_awards.col.face_value_of_loan,
            queryset=aggregate_awards.join(
                aggregate_faba.join(base_model, **{base_model_column: aggregate_faba.col.grouping_key}),
                **{base_model_column: aggregate_awards.col.grouping_key},
            )
            .with_cte(base_values)
            .with_cte(aggregate_faba)
            .with_cte(distinct_awards)
            .with_cte(aggregate_awards),
        )


class AwardTypeMixin:
    required_filters = ["def_codes", "award_type_codes"]

    @cached_property
    def award_type_codes(self):

        return self.filters.get("award_type_codes")


class FabaOutlayMixin:
    @property
    def outlay_field_annotation(self):
        return Coalesce(
            Sum(
                Case(
                    When(self.final_period_submission_query_filters, then=F("gross_outlay_amount_by_award_cpe")),
                    default=Value(0),
                )
            ),
            0,
        )

    def when_non_zero_award_spending(self, query):
        return query.annotate(
            total_outlay=self.outlay_field_annotation, total_obligation=Sum("transaction_obligated_amount")
        ).exclude(total_outlay=0, total_obligation=0)

    @property
    def unique_file_c(self):
        return Concat("piid", "parent_award_id", "fain", "uri")

    def unique_file_c_count(self):
        return Count(self.unique_file_c, distinct=True)


class SpendingMixin:
    required_filters = ["def_codes", "query"]

    @property
    def query(self):
        return self.filters.get("query")

    @cached_property
    def spending_type(self):
        model = [
            {
                "key": "spending_type",
                "name": "spending_type",
                "type": "enum",
                "enum_values": ["total", "award"],
                "allow_nulls": False,
                "optional": False,
            }
        ]

        return TinyShield(model).block(self.request.data)["spending_type"]


class LoansMixin:
    required_filters = ["def_codes", "query"]

    @property
    def query(self):
        return self.filters.get("query")

    @property
    def is_loan_award(self):
        return Q(award__type__in=loan_type_mapping)


class _BasePaginationMixin:
    def pagination(self):
        """pass"""

    def run_models(self, columns, default_sort_column="id"):
        model = customize_pagination_with_sort_columns(columns, default_sort_column)
        request_data = TinyShield(model).block(self.request.data.get("pagination", {}))
        return Pagination(
            page=request_data["page"],
            limit=request_data["limit"],
            lower_limit=(request_data["page"] - 1) * request_data["limit"],
            upper_limit=(request_data["page"] * request_data["limit"]),
            sort_key=request_data.get("sort", "obligation"),
            sort_order=request_data["order"],
            secondary_sort_key="id",
        )


class PaginationMixin(_BasePaginationMixin):
    @cached_property
    def pagination(self):
        sortable_columns = [
            "id",
            "code",
            "description",
            "award_count",
            "obligation",
            "outlay",
            "total_budgetary_resources",
        ]
        return self.run_models(sortable_columns)


class LoansPaginationMixin(_BasePaginationMixin):
    @cached_property
    def pagination(self):
        sortable_columns = ["id", "code", "description", "award_count", "obligation", "outlay", "face_value_of_loan"]
        return self.run_models(sortable_columns)
