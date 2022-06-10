from abc import ABC

from moonlan.dal.infrastructure.base_query_builders.base_query_builder import BaseQueryBuilder
from moonlan.dal.infrastructure.query_models.find_query import FindQuery


class FindQueryBuilder(BaseQueryBuilder, ABC):
    def _get_filter(self) -> dict:
        return {}

    def _get_projection(self) -> dict:
        return {}

    def _get_limit(self) -> int:
        return 0

    def _get_sort(self) -> list:
        return []

    def build(self) -> FindQuery:
        return FindQuery(
            filter=self._get_filter(),
            projection=self._get_projection(),
            limit=self._get_limit(),
            sort=self._get_sort()
        )
