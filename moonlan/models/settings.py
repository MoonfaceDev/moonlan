from pydantic import BaseModel


class ScanSettings(BaseModel):
    network_subnet: str | None
    scan_interval: int | None
    ports_to_scan: int | None


class ServerSettings(BaseModel):
    token_expiry_time: int | None
    gateway_ip: str | None
    gateway_mac: str | None


class Settings(BaseModel):
    scan_settings: ScanSettings | None
    server_settings: ServerSettings | None
