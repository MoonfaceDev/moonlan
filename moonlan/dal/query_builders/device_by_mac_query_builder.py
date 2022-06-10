from moonlan.dal.infrastructure.base_query_builders.find_one_query_builder import FindOneQueryBuilder


class DeviceByMacQueryBuilder(FindOneQueryBuilder):
    def __init__(self, mac_address: str):
        self._mac_address = mac_address

    def _get_filter(self) -> dict:
        return {
            'entity.mac': self._mac_address
        }
