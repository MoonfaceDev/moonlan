from _socket import getservbyport
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from pymongo import MongoClient

from moonlan.devices.device_manager import devices_config
from moonlan.exceptions import DeviceNotFoundError


class ScansData:
    def __init__(self, database_name: str):
        self._database = MongoClient().get_database(database_name)

    @staticmethod
    def _get_ports_with_service_names(ports: List[int]) -> List[Tuple[int, str]]:
        def safe_get_service_name(port: int) -> str:
            try:
                return getservbyport(port, "tcp")
            except OSError:
                return ''

        return [(port, safe_get_service_name(port)) for port in ports]

    @staticmethod
    def _get_device_response(document: Optional[Dict]) -> Dict:
        if document is None:
            raise DeviceNotFoundError()
        device = devices_config.devices.from_mac(document['entity']['mac'])
        response = {
            'last_online': document['scan_time'],
            'name': device.name,
            'type': device.type,
            'entity': document['entity']
        }
        return response

    def get_last(self) -> Dict:
        scans = self._database.get_collection('scans').aggregate([
            {
                '$sort': {'scan_time': -1}
            }, {
                '$limit': 1
            }, {
                '$project': {
                    '_id': 0,
                }
            }
        ])
        result = list(scans)[0]
        response = {
            'entities': [{
                'ip': entity['ip'],
                'device': devices_config.devices.from_mac(entity['mac']),
                'vendor': entity['vendor'],
                'open_ports': ScansData._get_ports_with_service_names(entity['open_ports'])
            } for entity in result['entities']],
            'scan_time': result['scan_time'],
        }
        return response

    def get_history(self, from_datetime: datetime, time_interval: float) -> Dict:
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
        response = {
            'devices': [{'time': entry['_id'], 'average': entry['avg']} for entry in result],
        }
        return response

    def get_ip(self, ip_address: str) -> Dict:
        device = self._database.get_collection('devices').find_one({
            'entity.ip': ip_address
        })
        return ScansData._get_device_response(device)

    def get_device(self, name: str) -> Dict:
        try:
            device = devices_config.devices[name]
        except KeyError:
            raise DeviceNotFoundError()
        device = self._database.get_collection('devices').find_one({
            'entity.mac': device.mac
        })
        return ScansData._get_device_response(device)

    def get_devices(self) -> List[Dict]:
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
