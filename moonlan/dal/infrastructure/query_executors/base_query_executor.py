from abc import ABC, abstractmethod
from typing import Any

from pymongo.collection import Collection

from moonlan.dal.infrastructure.query_models.base_query import BaseQuery


class BaseQueryExecutor(ABC):
    def __init__(self, collection: Collection):
        self._collection = collection

    @abstractmethod
    def execute(self, query: BaseQuery) -> Any:
        raise NotImplementedError()
