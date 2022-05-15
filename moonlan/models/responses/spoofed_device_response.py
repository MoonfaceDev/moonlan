from pydantic import BaseModel


class SpoofedDeviceResponse(BaseModel):
    mac: str
    ip: str
    forward: bool
