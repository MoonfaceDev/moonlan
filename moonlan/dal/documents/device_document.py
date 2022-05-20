from datetime import datetime

from pydantic import BaseModel


class EntityEmbeddedDocument(BaseModel):
    ip: str
    hostname: str
    mac: str
    vendor: str
    open_ports: list[int]


class DeviceDocument(BaseModel):
    entity: EntityEmbeddedDocument
    scan_time: datetime
