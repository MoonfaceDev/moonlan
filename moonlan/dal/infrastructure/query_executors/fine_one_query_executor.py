from moonlan.dal.infrastructure.query_executors.base_query_executor import BaseQueryExecutor
from moonlan.dal.infrastructure.query_models.find_one_query import FindOneQuery


class FindOneQueryExecutor(BaseQueryExecutor):
    def execute(self, query: FindOneQuery) -> dict:
        return self._collection.find_one(**query.dict())
