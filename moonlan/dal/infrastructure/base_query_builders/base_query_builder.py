from abc import ABC, abstractmethod

from moonlan.dal.infrastructure.query_models.base_query import BaseQuery


class BaseQueryBuilder(ABC):
    @abstractmethod
    def build(self) -> BaseQuery:
        raise NotImplementedError()
