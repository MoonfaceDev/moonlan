from moonlan.dal.infrastructure.base_query_builders.find_one_query_builder import FindOneQueryBuilder


class DeviceByIpQueryBuilder(FindOneQueryBuilder):
    def __init__(self, ip_address: str):
        self._ip_address = ip_address

    def _get_filter(self) -> dict:
        return {
            'entity.ip': self._ip_address
        }
