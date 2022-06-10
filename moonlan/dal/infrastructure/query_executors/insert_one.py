from typing import Callable

from pymongo.collection import Collection

from moonlan.dal.infrastructure.query_models.insert_one_query import InsertOneQuery


def insert_one(collection: Collection):
    def decorator(query_builder_function: Callable[[...], InsertOneQuery]):
        def decorated(*args, **kwargs):
            query = query_builder_function(*args, **kwargs)
            collection.insert_one(**query.dict())

        return decorated

    return decorator
