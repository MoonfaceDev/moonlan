from abc import ABC, abstractmethod

from moonlan.dal.infrastructure.base_query_builders.base_query_builder import BaseQueryBuilder
from moonlan.dal.infrastructure.query_models.find_one_query import FindOneQuery


class FindOneQueryBuilder(BaseQueryBuilder, ABC):
    @abstractmethod
    def _get_filter(self) -> dict:
        raise NotImplementedError()

    def _get_projection(self) -> dict:
        return {}

    def _get_sort(self) -> list:
        return []

    def build(self) -> FindOneQuery:
        return FindOneQuery(
            filter=self._get_filter(),
            projection=self._get_projection(),
            sort=self._get_sort()
        )
