from typing import Callable, Type, Iterator

from pydantic import BaseModel
from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor

from moonlan.dal.infrastructure.query_models.aggregation_query import AggregationQuery


def _document_generator(cursor: CommandCursor[dict], document_type: Type[BaseModel]):
    while True:
        try:
            document = next(cursor)
            yield document_type(**document)
        except StopIteration:
            return


def aggregate(collection: Collection, document_type: Type[BaseModel]):
    def decorator(query_builder_function: Callable[[...], AggregationQuery]):
        def decorated(*args, **kwargs) -> Iterator[document_type]:
            query = query_builder_function(*args, **kwargs)
            cursor = collection.aggregate(**query.dict())
            document_iterator = _document_generator(cursor, document_type)
            return document_iterator

        return decorated

    return decorator
