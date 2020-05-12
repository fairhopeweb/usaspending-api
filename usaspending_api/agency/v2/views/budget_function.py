from django.db.models import Q, Sum
from rest_framework.request import Request
from rest_framework.response import Response
from typing import Any
from usaspending_api.agency.v2.views.agency_base import AgencyBase
from usaspending_api.common.cache_decorator import cache_response
from usaspending_api.common.helpers.generic_helper import get_simple_pagination_metadata
from usaspending_api.financial_activities.models import FinancialAccountsByProgramActivityObjectClass


class BudgetFunctionList(AgencyBase):
    """
    Obtain the count of budget functions for a specific agency in a single
    fiscal year based on whether or not that budget function has ever
    been submitted in File B.
    """

    endpoint_doc = "usaspending_api/api_contracts/contracts/v2/agency/toptier_code/budget_function/budget_function.md"

    def validate_request(self):
        return None

    def format_results(self, rows):
        names = set([row["treasury_account__budget_function_title"] for row in rows])
        budget_functions = [{"name": x} for x in names]
        for item in budget_functions:
            item["children"] = [
                {
                    "name": row["treasury_account__budget_subfunction_title"],
                    "obligated_amount": row["obligated_amount"],
                    "gross_outlay_amount": row["gross_outlay_amount"],
                }
                for row in rows
                if item["name"] == row["treasury_account__budget_function_title"]
            ]
            item["obligated_amount"] = sum([x["obligated_amount"] for x in item["children"]])
            item["gross_outlay_amount"] = sum([x["gross_outlay_amount"] for x in item["children"]])
        order = self.pagination.sort_order == "desc"
        budget_functions = sorted(budget_functions, key=lambda x: x[self.pagination.sort_key], reverse=order)
        return budget_functions

    @cache_response()
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        results = self.format_results(list(self.get_budget_function_queryset(request)))[
            self.pagination.lower_limit : self.pagination.upper_limit
        ]
        page_metadata = get_simple_pagination_metadata(len(results), self.pagination.limit, self.pagination.page)
        return Response(
            {
                "toptier_code": self.toptier_code,
                "fiscal_year": self.fiscal_year,
                "limit": self.pagination.limit,
                "results": results[:self.pagination.limit],
                "messages": self.standard_response_messages,
                "page_metadata": page_metadata,
            }
        )

    def get_budget_function_queryset(self, request):
        filters = [~Q(treasury_account__budget_function_code=""), ~Q(treasury_account__budget_function_code=None)]
        if request.data.get("filter") is not None:
            filters.append(
                Q(
                    Q(treasury_account__budget_function_title__icontains=request.data["filter"])
                    | Q(treasury_account__budget_subfunction_title__icontains=request.data["filter"])
                )
            )

        results = (
            (
                FinancialAccountsByProgramActivityObjectClass.objects.filter(
                    final_of_fy=True,
                    treasury_account__funding_toptier_agency=self.toptier_agency,
                    submission__reporting_fiscal_year=self.fiscal_year,
                )
                .exclude(
                    obligations_incurred_by_program_object_class_cpe=0,
                    gross_outlay_amount_by_program_object_class_cpe=0,
                )
                .filter(*filters)
            )
            .values(
                "treasury_account__budget_function_code",
                "treasury_account__budget_function_title",
                "treasury_account__budget_subfunction_code",
                "treasury_account__budget_subfunction_title",
            )
            .annotate(
                obligated_amount=Sum("obligations_incurred_by_program_object_class_cpe"),
                gross_outlay_amount=Sum("gross_outlay_amount_by_program_object_class_cpe"),
            )
        )
        return results
