from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient

from moonlan.config import config

_database = MongoClient().get_database(config.database.database_name)


def get_history(from_datetime: datetime, time_interval: float) -> list:
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
    return list(history)


def get_device_by_ip(ip_address: str) -> Mapping[str, Any]:
    document = _database.get_collection('devices').find_one({
        'entity.ip': ip_address
    })
    return document


def get_device_by_mac(mac_address: str) -> Mapping[str, Any]:
    document = _database.get_collection('devices').find_one({
        'entity.mac': mac_address
    })
    return document


def get_devices() -> list[dict]:
    devices = _database.get_collection('devices').find()
    return list(devices)
