from moonlan.dal.infrastructure.query_models.base_query import BaseQuery


class FindQuery(BaseQuery):
    filter: dict
    projection: dict | None
    limit: int | None
    sort: list | None
