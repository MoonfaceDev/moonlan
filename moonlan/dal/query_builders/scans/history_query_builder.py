from datetime import datetime, timezone

from moonlan.dal.infrastructure.base_query_builders.aggregation_query_builder import AggregationQueryBuilder
from moonlan.dal.infrastructure.exceptions import QueryBuildingError


class HistoryQueryBuilder(AggregationQueryBuilder):
    def __init__(self, start_datetime: datetime, end_datetime: datetime, time_interval: float):
        self._start_datetime = start_datetime
        self._end_datetime = end_datetime
        self._time_interval = time_interval

    def _get_boundaries(self) -> list[int]:
        return [1000 * boundary for boundary in range(
            int(self._start_datetime.replace(tzinfo=timezone.utc).timestamp()),
            int(self._end_datetime.replace(tzinfo=timezone.utc).timestamp() + self._time_interval),
            int(self._time_interval))]

    def _get_datetime_match(self) -> dict:
        return {'$match': {
            '$and': [
                {'scan_time': {'$gt': datetime.fromtimestamp(
                    self._start_datetime.timestamp() -
                    self._start_datetime.replace(tzinfo=timezone.utc).timestamp() % self._time_interval
                )}},
                {'scan_time': {'$lt': datetime.fromtimestamp(
                    self._end_datetime.timestamp() -
                    self._end_datetime.replace(tzinfo=timezone.utc).timestamp() % self._time_interval
                )}}
            ]
        }}

    def _get_facet(self, boundaries: list[int]) -> dict:
        return {'$facet': {'data': [{'$bucket': {
            'groupBy': {
                '$subtract': [
                    {'$toLong': '$scan_time'},
                    {'$mod': [{'$toLong': '$scan_time'}, int(self._time_interval * 1000)]}
                ]
            },
            'boundaries': boundaries,
            'default': 'Other',
            'output': {
                'avg': {'$avg': {'$size': '$entities'}}
            }
        }}]}}

    @classmethod
    def _get_add_data_field(cls, boundaries: list[int]):
        return {"$addFields": {"data": {"$map": {
            "input": boundaries[:-1],
            "as": "i",
            "in": {
                "_id": "$$i",
                "avg": {
                    "$cond": [
                        {"$eq": [{"$indexOfArray": ["$data._id", "$$i"]}, -1]},
                        0,
                        {"$arrayElemAt": ["$data.avg", {"$indexOfArray": ["$data._id", "$$i"]}]}
                    ]
                }
            }
        }}}}

    @classmethod
    def _get_unwind_data(cls) -> dict:
        return {"$unwind": "$data"}

    @classmethod
    def _get_replace_root_to_data(cls) -> dict:
        return {"$replaceRoot": {"newRoot": "$data"}}

    @classmethod
    def _get_final_project(cls) -> dict:
        return {'$project': {
            '_id': {
                '$toDate': '$_id'
            },
            'avg': 1
        }}

    @classmethod
    def _get_final_sort(cls) -> dict:
        return {'$sort': {
            '_id': 1
        }}

    def _get_pipeline(self) -> list[dict]:
        boundaries = self._get_boundaries()
        if len(boundaries) < 2:
            raise QueryBuildingError('No buckets exist between start to end datetime')
        return [
            self._get_datetime_match(),
            self._get_facet(boundaries),
            self._get_add_data_field(boundaries),
            self._get_unwind_data(),
            self._get_replace_root_to_data(),
            self._get_final_project(),
            self._get_final_sort()
        ]
