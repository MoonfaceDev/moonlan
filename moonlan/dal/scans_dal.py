from datetime import datetime

from pymongo import MongoClient

from moonlan.config import config
from moonlan.dal.documents.device_scan_document import DeviceScanDocument
from moonlan.dal.documents.history_document import HistoryDocument
from moonlan.dal.documents.scan_time_document import ScanTimeDocument
from moonlan.dal.infrastructure.query_executors.aggregate import aggregate
from moonlan.dal.infrastructure.query_executors.find_one import find_one
from moonlan.dal.query_builders.scans.device_scans_query_builder import DeviceScansQueryBuilder
from moonlan.dal.query_builders.scans.history_query_builder import HistoryQueryBuilder
from moonlan.dal.query_builders.scans.last_scan_time_query_builder import LastScanTimeQueryBuilder

collection = MongoClient().get_database(config.database.database_name).get_collection('scans')


@aggregate(collection, HistoryDocument)
def get_history(start_datetime: datetime, end_datetime: datetime, time_interval: float):
    return HistoryQueryBuilder(start_datetime, end_datetime, time_interval).build()


@aggregate(collection, DeviceScanDocument)
def get_scans_for_device(mac: str, start_datetime: datetime, end_datetime: datetime):
    return DeviceScansQueryBuilder(mac, start_datetime, end_datetime).build()


@find_one(collection, ScanTimeDocument)
def get_last_scan_time():
    return LastScanTimeQueryBuilder().build()
