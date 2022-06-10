from typing import Type, Callable

from pydantic import BaseModel
from pymongo.collection import Collection

from moonlan.dal.infrastructure.exceptions import DocumentNotFoundError
from moonlan.dal.infrastructure.query_models.find_one_query import FindOneQuery


def find_one(collection: Collection, document_type: Type[BaseModel]):
    def decorator(query_builder_function: Callable[[...], FindOneQuery]):
        def decorated(*args, **kwargs) -> document_type:
            query = query_builder_function(*args, **kwargs)
            document = collection.find_one(**query.dict())
            if document is None:
                raise DocumentNotFoundError()
            return document_type(**document)

        return decorated

    return decorator
