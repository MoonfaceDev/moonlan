from pymongo.command_cursor import CommandCursor

from moonlan.dal.infrastructure.query_executors.base_query_executor import BaseQueryExecutor
from moonlan.dal.infrastructure.query_models.aggregation_query import AggregationQuery


class AggregationQueryExecutor(BaseQueryExecutor):
    def execute(self, query: AggregationQuery) -> CommandCursor[dict]:
        return self._collection.aggregate(**query.dict())
