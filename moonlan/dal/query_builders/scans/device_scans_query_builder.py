from datetime import datetime

from moonlan.dal.infrastructure.base_query_builders.aggregation_query_builder import AggregationQueryBuilder


class DeviceScansQueryBuilder(AggregationQueryBuilder):
    def __init__(self, mac: str, start_datetime: datetime, end_datetime: datetime):
        self._mac = mac
        self._start_datetime = start_datetime
        self._end_datetime = end_datetime

    def _get_datetime_match(self) -> dict:
        return {'$match': {
            '$and': [
                {'scan_time': {'$gte': self._start_datetime}},
                {'scan_time': {'$lte': self._end_datetime}},
            ]
        }}

    def _get_set_online(self) -> dict:
        return {'$set': {'online': {
            '$gt': [
                {'$size': {
                    '$filter': {'input': '$entities', 'as': 'entity', 'cond': {'$eq': ['$$entity.mac', self._mac]}}
                }},
                0
            ]
        }}}

    @classmethod
    def _get_final_project(cls) -> dict:
        return {'$project': {'_id': 0, 'scan_time': 1, 'online': 1}}

    @classmethod
    def _get_final_sort(cls) -> dict:
        return {'$sort': {'scan_time': 1}}

    def _get_pipeline(self) -> list:
        return [
            self._get_datetime_match(),
            self._get_set_online(),
            self._get_final_project(),
            self._get_final_sort()
        ]
