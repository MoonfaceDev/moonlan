import json
from pathlib import Path

from pydantic import BaseModel


def _load_config(config_path: Path) -> dict[str, dict[str, str]]:
    with config_path.open('r') as file:
        return json.load(file)


class Authentication(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class Database(BaseModel):
    database_name: str


class Spoofing(BaseModel):
    gateway_ip: str
    gateway_mac: str
    ip_forward_file_path: str


class Server(BaseModel):
    allowed_origins: list[str]


class Config(BaseModel):
    authentication: Authentication
    database: Database
    spoofing: Spoofing
    server: Server


config = Config(**_load_config(Path('/etc/moonitor/api/config.json').expanduser()))
