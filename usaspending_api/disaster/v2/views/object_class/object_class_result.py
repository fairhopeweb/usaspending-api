from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Dict

from usaspending_api.common.data_classes import Pagination
from usaspending_api.disaster.v2.views.data_classes import Collation, Element


class MinorClass(Element):
    """Renaming the original generic object to clearly be TAS"""


class MajorClass(Collation):
    """Renaming the original generic object to clearly be Federal Account"""


@dataclass_json
@dataclass
class FedAcctResults:
    _federal_accounts: Dict[MinorClass, MinorClass] = field(default_factory=dict)

    def __getitem__(self, key):
        return self._federal_accounts.setdefault(key, key)

    def __len__(self):
        return len(self._federal_accounts)

    def rollup(self):
        for row in self._federal_accounts:
            for child in row.children:
                row.outlay += child.outlay
                row.obligation += child.obligation
                row.count += child.count

    def sort(self, field, direction):
        for row in self._federal_accounts:
            row.children = self.sort_results(row.children, field, direction)

        self._federal_accounts = self.sort_results(self._federal_accounts, field, direction)

    def slice(self, start, end):
        results = []
        for i, fa in enumerate(self._federal_accounts):
            if i >= start and i < end:
                results.append(fa)
        return results

    def finalize(self, pagination: Pagination):
        self.rollup()
        self.sort(pagination.sort_key, pagination.sort_order)
        results = list(fa.to_dict() for fa in self.slice(pagination.lower_limit, pagination.upper_limit))
        for result in results:
            result.pop("total_budgetary_resources")
        return results

    @staticmethod
    def sort_results(items, field, direction="desc"):
        reverse = True
        if direction == "asc":
            reverse = False

        if isinstance(items, list):
            return sorted(items, key=lambda x: getattr(x, field), reverse=reverse)
        else:
            return {k: items[k] for k in sorted(items, key=lambda x: getattr(x, field), reverse=reverse)}
