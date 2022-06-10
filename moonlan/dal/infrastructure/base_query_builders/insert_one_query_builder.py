from abc import abstractmethod

from moonlan.dal.infrastructure.base_query_builders.base_query_builder import BaseQueryBuilder
from moonlan.dal.infrastructure.query_models.insert_one_query import InsertOneQuery


class InsertOneQueryBuilder(BaseQueryBuilder):
    @abstractmethod
    def _get_document(self) -> dict:
        raise NotImplementedError()

    def build(self) -> InsertOneQuery:
        return InsertOneQuery(document=self._get_document())
