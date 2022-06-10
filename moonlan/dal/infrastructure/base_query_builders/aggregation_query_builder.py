from abc import ABC, abstractmethod

from moonlan.dal.infrastructure.base_query_builders.base_query_builder import BaseQueryBuilder
from moonlan.dal.infrastructure.query_models.aggregation_query import AggregationQuery


class AggregationQueryBuilder(BaseQueryBuilder, ABC):
    @abstractmethod
    def _get_pipeline(self) -> list:
        raise NotImplementedError()

    def build(self) -> AggregationQuery:
        return AggregationQuery(pipeline=self._get_pipeline())
