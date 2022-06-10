from datetime import datetime

from pymongo import MongoClient

from moonlan.config import config
from moonlan.dal.documents.device_document import DeviceDocument
from moonlan.dal.documents.device_scan_document import DeviceScanDocument
from moonlan.dal.documents.history_document import HistoryDocument
from moonlan.dal.documents.scan_time_document import ScanTimeDocument
from moonlan.dal.infrastructure.query_executors.aggregation_query_executor import AggregationQueryExecutor
from moonlan.dal.infrastructure.query_executors.find_query_executor import FindQueryExecutor
from moonlan.dal.infrastructure.query_executors.fine_one_query_executor import FindOneQueryExecutor
from moonlan.dal.query_builders.device_by_ip_query_builder import DeviceByIpQueryBuilder
from moonlan.dal.query_builders.device_by_mac_query_builder import DeviceByMacQueryBuilder
from moonlan.dal.query_builders.device_scans_query_builder import DeviceScansQueryBuilder
from moonlan.dal.query_builders.devices_query_builder import DevicesQueryBuilder
from moonlan.dal.query_builders.history_query_builder import HistoryQueryBuilder
from moonlan.dal.query_builders.last_scan_time_query_builder import LastScanTimeQueryBuilder

_database = MongoClient().get_database(config.database.database_name)


def get_history(start_datetime: datetime, end_datetime: datetime, time_interval: float) -> list[HistoryDocument]:
    query = HistoryQueryBuilder(start_datetime, end_datetime, time_interval).build()
    documents = AggregationQueryExecutor(_database.get_collection('scans')).execute(query)
    return [HistoryDocument(**document) for document in documents]


def get_scans_for_device(mac: str, start_datetime: datetime, end_datetime: datetime) -> list[DeviceScanDocument]:
    query = DeviceScansQueryBuilder(mac, start_datetime, end_datetime).build()
    documents = AggregationQueryExecutor(_database.get_collection('scans')).execute(query)
    return [DeviceScanDocument(**document) for document in documents]


def get_device_by_ip(ip_address: str) -> DeviceDocument:
    query = DeviceByIpQueryBuilder(ip_address).build()
    document = FindOneQueryExecutor(_database.get_collection('devices')).execute(query)
    return DeviceDocument(**document)


def get_device_by_mac(mac_address: str) -> DeviceDocument:
    query = DeviceByMacQueryBuilder(mac_address).build()
    document = FindOneQueryExecutor(_database.get_collection('devices')).execute(query)
    return DeviceDocument(**document)


def get_devices() -> list[DeviceDocument]:
    query = DevicesQueryBuilder().build()
    documents = FindQueryExecutor(_database.get_collection('devices')).execute(query)
    return [DeviceDocument(**document) for document in documents]


def get_last_scan_time() -> ScanTimeDocument:
    query = LastScanTimeQueryBuilder().build()
    document = FindOneQueryExecutor(_database.get_collection('scans')).execute(query)
    return ScanTimeDocument(**document)
