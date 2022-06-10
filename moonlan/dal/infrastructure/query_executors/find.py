from typing import Type, Callable, Iterator

from pydantic import BaseModel
from pymongo.collection import Collection
from pymongo.cursor import Cursor

from moonlan.dal.infrastructure.query_models.find_query import FindQuery


def _document_generator(cursor: Cursor[dict], document_type: Type[BaseModel]):
    while True:
        try:
            document = next(cursor)
            yield document_type(**document)
        except StopIteration:
            return


def find(collection: Collection, document_type: Type[BaseModel]):
    def decorator(query_builder_function: Callable[[...], FindQuery]):
        def decorated(*args, **kwargs) -> Iterator[document_type]:
            query = query_builder_function(*args, **kwargs)
            cursor = collection.find(**query.dict())
            document_iterator = _document_generator(cursor, document_type)
            return document_iterator

        return decorated

    return decorator
