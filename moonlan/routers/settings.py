import asyncio
import json

from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from moonlan import consts
from moonlan.dependencies.authentication_dependency import current_active_user
from moonlan.models.settings import ServerSettings, ScanSettings, Settings

router = APIRouter(prefix='/settings', tags=['Settings'], dependencies=[Depends(current_active_user)])


@router.get('/all', response_model=Settings)
async def get_all():
    with consts.Settings.SCAN_CONFIG_PATH.open('r') as file:
        scan_settings_raw = json.load(file)
    scan_settings = ScanSettings(
        network_subnet=scan_settings_raw['network_scan']['network_subnet'],
        scan_interval=scan_settings_raw['network_scan']['scan_interval'],
        ports_to_scan=scan_settings_raw['entity_scan']['ports_to_scan']
    )
    with consts.Settings.SERVER_CONFIG_PATH.open('r') as file:
        server_settings_raw = json.load(file)
    server_settings = ServerSettings(
        token_expiry_time=int(server_settings_raw['authentication']['access_token_expire_minutes']),
        gateway_ip=server_settings_raw['spoofing']['gateway_ip'],
        gateway_mac=server_settings_raw['spoofing']['gateway_mac']
    )
    return Settings(scan_settings=scan_settings, server_settings=server_settings)


def _update_scan_settings(scan_settings: ScanSettings):
    with consts.Settings.SCAN_CONFIG_PATH.open('r') as file:
        scan_settings_raw = json.load(file)
    scan_settings_raw['network_scan']['network_subnet'] = scan_settings.network_subnet
    scan_settings_raw['network_scan']['scan_interval'] = scan_settings.scan_interval
    scan_settings_raw['entity_scan']['ports_to_scan'] = scan_settings.ports_to_scan
    with consts.Settings.SCAN_CONFIG_PATH.open('w') as file:
        json.dump(scan_settings_raw, file)


def _update_server_settings(server_settings: ServerSettings):
    with consts.Settings.SERVER_CONFIG_PATH.open('r') as file:
        server_settings_raw = json.load(file)
    server_settings_raw['authentication']['access_token_expire_minutes'] = str(server_settings.token_expiry_time)
    server_settings_raw['spoofing']['gateway_ip'] = server_settings.gateway_ip
    server_settings_raw['spoofing']['gateway_mac'] = server_settings.gateway_mac
    with consts.Settings.SERVER_CONFIG_PATH.open('w') as file:
        json.dump(server_settings_raw, file)


@router.post('/update')
async def update_all(settings: Settings):
    _update_scan_settings(settings.scan_settings)
    _update_server_settings(settings.server_settings)


async def _restart_service(service_name: str):
    # WARNING: DON'T ALLOW SERVICE NAME FROM USER INPUT
    proc = await asyncio.create_subprocess_shell(
        f'systemctl restart {service_name}')
    stdout, stderr = await proc.communicate()
    return proc.returncode, stdout, stderr


@router.post('/restart/scan')
async def restart_scan(background_tasks: BackgroundTasks):
    background_tasks.add_task(_restart_service, consts.Settings.SCAN_SERVICE_NAME)
    return


@router.post('/restart/server')
async def restart_server(background_tasks: BackgroundTasks):
    background_tasks.add_task(_restart_service, consts.Settings.SERVER_SERVICE_NAME)
    return

