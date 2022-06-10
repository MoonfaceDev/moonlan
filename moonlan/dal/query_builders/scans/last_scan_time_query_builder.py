from moonlan.dal.infrastructure.base_query_builders.find_one_query_builder import FindOneQueryBuilder


class LastScanTimeQueryBuilder(FindOneQueryBuilder):
    def _get_filter(self) -> dict:
        return {}

    def _get_projection(self) -> dict:
        return {'_id': 0, 'scan_time': 1}

    def _get_sort(self) -> list:
        return [('scan_time', -1)]
