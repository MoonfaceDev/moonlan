from moonlan.dal.infrastructure.query_models.base_query import BaseQuery


class FindOneQuery(BaseQuery):
    filter: dict
    projection: dict | None
    sort: list | None
