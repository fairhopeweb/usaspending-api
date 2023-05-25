from usaspending_api.common.filters.time_period.time_period import AbstractTimePeriod
from usaspending_api.search.filters.elasticsearch.filter import _QueryType

NEW_AWARDS_ONLY_KEYWORD = "new_awards_only"


class NewAwardsOnlyTimePeriod(AbstractTimePeriod):
    """A decorator class that can be used to apply a new awards only filter
    ON TOP of an existing time period filter.
    """

    def __init__(self, transaction_search_time_period_obj, query_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._query_type = query_type
        self._transaction_search_time_period_obj = transaction_search_time_period_obj

    @property
    def _additional_lte_filters_for_new_awards_only(self):
        # Making this variable a property to ensure it grabs
        # end date on the fly in case it wasn't set beofre
        # instantiating this class.
        return {
            _QueryType.TRANSACTIONS: [
                {"action_date": {"lte": self.end_date()}},
                {"award_date_signed": {"lte": self.end_date()}},
            ]
        }

    @property
    def _additional_gte_filters_for_new_awards_only(self):
        # Making this variable a property to ensure it grabs
        # end date on the fly in case it wasn't set beofre
        # instantiating this class.
        return {
            _QueryType.TRANSACTIONS: [
                {"action_date": {"gte": self.start_date()}},
                {"award_date_signed": {"gte": self.start_date()}},
            ]
        }

    @property
    def filter_value(self):
        return self._transaction_search_time_period_obj.filter_value

    @filter_value.setter
    def filter_value(self, filter_value: dict):
        self._transaction_search_time_period_obj.filter_value = filter_value

    def start_date(self):
        return self._transaction_search_time_period_obj.start_date()

    def end_date(self):
        return self._transaction_search_time_period_obj.end_date()

    def gte_date_type(self):
        return self._transaction_search_time_period_obj.gte_date_type()

    def lte_date_type(self):
        return self._transaction_search_time_period_obj.lte_date_type()

    def gte_date_range(self):
        wrapped_range = self._transaction_search_time_period_obj.gte_date_range()
        if self._new_awards_only():
            # When date type is new awards only we don't use date type directly in
            # the range
            wrapped_range = []
            for additional_filter in self._additional_gte_filters_for_new_awards_only[self._query_type]:
                wrapped_range.append(additional_filter)
        return wrapped_range

    def lte_date_range(self):
        wrapped_range = self._transaction_search_time_period_obj.lte_date_range()
        if self._new_awards_only():
            # When date type is new awards only we don't use date type directly in
            # the range
            wrapped_range = []
            for additional_filter in self._additional_lte_filters_for_new_awards_only[self._query_type]:
                wrapped_range.append(additional_filter)
        return wrapped_range

    def _new_awards_only(self):
        """Indicates if the time period filter requires only new awards.

        Returns:
            bool
        """
        return self._transaction_search_time_period_obj.filter_value.get("date_type") == NEW_AWARDS_ONLY_KEYWORD
