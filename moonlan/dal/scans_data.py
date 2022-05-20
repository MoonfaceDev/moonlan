from datetime import datetime, timezone, timedelta

from pymongo import MongoClient

from moonlan.config import config
from moonlan.dal.documents.device_document import DeviceDocument
from moonlan.dal.documents.history_document import HistoryDocument
from moonlan.dal.documents.device_scan_document import DeviceScanDocument

_database = MongoClient().get_database(config.database.database_name)


def get_history(from_datetime: datetime, time_interval: float) -> list[HistoryDocument]:
    history = _database.get_collection('scans').aggregate([
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
    return [HistoryDocument(**document) for document in history]


def get_scans_for_device(
        mac: str,
        from_datetime: datetime,
        time_interval: timedelta
) -> list[DeviceScanDocument]:
    history = _database.get_collection('scans').aggregate([
        {'$match': {
            'scan_time': {'$gt': datetime.fromtimestamp(
                from_datetime.timestamp()
                - from_datetime.replace(tzinfo=timezone.utc).timestamp() % time_interval.seconds
            )}
        }},
        {'$set': {'online': {
            '$gt': [
                {'$size': {
                    '$filter': {'input': '$entities', 'as': 'entity', 'cond': {'$eq': ['$$entity.mac', mac]}}
                }},
                0
            ]
        }}},
        {'$project': {'_id': 0, 'scan_time': 1, 'online': 1}},
        {'$sort': {'scan_time': 1}}
    ])
    return [DeviceScanDocument(**document) for document in history]


def get_device_by_ip(ip_address: str) -> DeviceDocument:
    document = _database.get_collection('devices').find_one({
        'entity.ip': ip_address
    })
    return DeviceDocument(**document)


def get_device_by_mac(mac_address: str) -> DeviceDocument:
    document = _database.get_collection('devices').find_one({
        'entity.mac': mac_address
    })
    return DeviceDocument(**document)


def get_devices() -> list[DeviceDocument]:
    devices = _database.get_collection('devices').find()
    return [DeviceDocument(**document) for document in devices]
