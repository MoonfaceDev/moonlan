from moonlan.dal.infrastructure.query_models.base_query import BaseQuery


class InsertOneQuery(BaseQuery):
    document: dict
