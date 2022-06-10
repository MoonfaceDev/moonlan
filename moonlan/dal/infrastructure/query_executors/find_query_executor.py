from pymongo.cursor import Cursor

from moonlan.dal.infrastructure.query_executors.base_query_executor import BaseQueryExecutor
from moonlan.dal.infrastructure.query_models.find_query import FindQuery


class FindQueryExecutor(BaseQueryExecutor):
    def execute(self, query: FindQuery) -> Cursor[dict]:
        return self._collection.find(**query.dict())
