from _socket import getservbyport
from datetime import datetime, timezone

from pymongo import MongoClient

from moonlan.devices.device_manager import devices_config
from moonlan.exceptions import DeviceNotFoundError


class ScansData:
    def __init__(self, database_name: str):
        self._database = MongoClient().get_database(database_name)

    @staticmethod
    def _get_ports_with_service_names(ports: list[int]) -> list[tuple[int, str]]:
        def safe_get_service_name(port: int) -> str:
            try:
                return getservbyport(port, "tcp")
            except OSError:
                return ''

        return [(port, safe_get_service_name(port)) for port in ports]

    @staticmethod
    def _get_device_response(document: dict | None) -> dict:
        if document is None:
            raise DeviceNotFoundError()
        device = devices_config.devices.from_mac(document['entity']['mac'])
        response = {
            'last_online': document['scan_time'],
            'name': device.name,
            'type': device.type,
            **document['entity']
        }
        return response

    def get_history(self, from_datetime: datetime, time_interval: float) -> list:
        history = self._database.get_collection('scans').aggregate([
            {'$match': {
                'scan_time': {'$gt': datetime.fromtimestamp(
                    from_datetime.timestamp() - from_datetime.replace(tzinfo=timezone.utc).timestamp() % time_interval)}
            }},
            {'$group': {
                '_id': {
                    '$toDate': {
                        '$subtract': [
                            {'$toLong': '$scan_time'},
                            {'$mod': [{'$toLong': '$scan_time'}, int(time_interval * 1000)]}
                        ]
                    }
                },
                'avg': {'$avg': {'$size': '$entities'}}
            }},
            {'$sort': {
                '_id': 1
            }}
        ])
        result = list(history)
        response = [{'time': entry['_id'], 'average': entry['avg']} for entry in result]
        return response

    def get_ip(self, ip_address: str) -> dict:
        device = self._database.get_collection('devices').find_one({
            'entity.ip': ip_address
        })
        return ScansData._get_device_response(device)

    def get_device(self, name: str) -> dict:
        try:
            device = devices_config.devices[name]
        except KeyError:
            raise DeviceNotFoundError()
        device = self._database.get_collection('devices').find_one({
            'entity.mac': device.mac
        })
        return ScansData._get_device_response(device)

    def get_devices(self) -> list[dict]:
        devices = self._database.get_collection('devices').find()
        response = [{
            'entity': {
                'ip': device['entity']['ip'],
                'device': devices_config.devices.from_mac(device['entity']['mac']),
                'vendor': device['entity']['vendor'],
                'open_ports': ScansData._get_ports_with_service_names(device['entity']['open_ports'])
            },
            'last_online': device['scan_time']
        } for device in devices]
        return response
