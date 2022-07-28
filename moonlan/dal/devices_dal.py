from pymongo import MongoClient

from moonlan import consts
from moonlan.config import config
from moonlan.dal.documents.device_document import DeviceDocument
from moonlan.dal.infrastructure.query_executors.find import find
from moonlan.dal.infrastructure.query_executors.find_one import find_one
from moonlan.dal.query_builders.devices.device_by_ip_query_builder import DeviceByIpQueryBuilder
from moonlan.dal.query_builders.devices.device_by_mac_query_builder import DeviceByMacQueryBuilder
from moonlan.dal.query_builders.devices.devices_query_builder import DevicesQueryBuilder

collection = MongoClient(consts.Database.HOSTNAME).get_database(config.database.database_name).get_collection(
    consts.Database.DEVICES_COLLECTION_NAME
)


@find_one(collection, DeviceDocument)
def get_device_by_ip(ip_address: str):
    return DeviceByIpQueryBuilder(ip_address).build()


@find_one(collection, DeviceDocument)
def get_device_by_mac(mac_address: str):
    return DeviceByMacQueryBuilder(mac_address).build()


@find(collection, DeviceDocument)
def get_devices():
    return DevicesQueryBuilder().build()
