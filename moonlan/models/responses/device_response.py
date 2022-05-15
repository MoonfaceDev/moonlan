from datetime import datetime

from pydantic import BaseModel


class DeviceResponse(BaseModel):
    last_online: datetime
    name: str
    type: str
    ip: str
    hostname: str
    mac: str
    vendor: str
    open_ports: list[tuple[int, str]]
