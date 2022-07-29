from pathlib import Path


class ArpSpoofing:
    IP_FORWARD_TRUE = '1\n'
    IP_FORWARD_FALSE = '0\n'
    ARP_REPLY_OPCODE = 2
    ARP_PACKET_INTERVAL = 2  # seconds
    ARP_RECOVERY_PACKET_COUNT = 5
    SPOOFED_DEVICE_MAC_KEY = 'mac'
    SPOOFED_DEVICE_IP_KEY = 'ip'
    SPOOFED_DEVICE_FORWARD_KEY = 'forward'
    SPOOFED_DEVICE_DEFAULT_MAC = ''
    SPOOFED_DEVICE_DEFAULT_IP = ''
    SPOOFED_DEVICE_DEFAULT_FORWARD = False


class Authentication:
    PASSWORD_HASHING_SCHEME = 'bcrypt'
    JWT_EXPIRY_KEY = 'exp'
    JWT_EMAIL_KEY = 'sub'
    ACCESS_TOKEN_TYPE = 'bearer'
    AUTHENTICATE_HEADER_VALUE = 'Bearer'
    AUTHENTICATE_HEADER_NAME = 'WWW-Authenticate'


class Config:
    CONFIG_PATH = Path('/etc/moonitor/api/config.json')


class Database:
    DEVICES_COLLECTION_NAME = 'devices'
    SCANS_COLLECTION_NAME = 'scans'
    USERS_COLLECTION_NAME = 'users'


class DeviceAPI:
    PORT_SERVICE_PROTOCOL = 'tcp'
    PORT_DEFAULT_SERVICE = ''


class DeviceManager:
    DEVICES_CONFIG_PATH = Path('/etc/moonitor/api/devices.json')
    DEFAULT_NAME = 'UNKNOWN'
    DEFAULT_TYPE = 'Unknown'
    VIEW_FILE_CONTENT_TYPE = 'application/json'


class Server:
    FRONTEND_PATH = Path('/etc/moonitor/app')
    FRONTEND_STATIC_PATH = Path('/etc/moonitor/app/static')
    FRONTEND_INDEX_FILE_NAME = 'index.html'
    TEMPLATE_REQUEST_KEY = 'request'


class Settings:
    SCAN_CONFIG_PATH = Path('/etc/moonitor/scan/config.json')
    SERVER_CONFIG_PATH = Path('/etc/moonitor/api/config.json')
    SCAN_SERVICE_NAME = 'moonscan'
    SERVER_SERVICE_NAME = 'moonlan'
    SUCCESS_RETURN_CODE = 0
