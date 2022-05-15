from _socket import getservbyport
from collections.abc import Mapping
from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from moonlan import scans_data
from moonlan.authentication_api import current_active_user
from moonlan.devices.device_manager import devices_config
from moonlan.models.responses.device_response import DeviceResponse
from moonlan.models.responses.devices_response import DevicesResponse
from moonlan.models.responses.history_response import HistoryResponse

router = APIRouter(prefix='/device', tags=['Devices'], dependencies=[Depends(current_active_user)])


def _get_ports_with_service_names(ports: list[int]) -> list[dict]:
    def safe_get_service_name(port: int) -> str:
        try:
            return getservbyport(port, "tcp")
        except OSError:
            return ''

    return [{'port': port, 'service': safe_get_service_name(port)} for port in ports]


def _get_device_response(device: Mapping[str, Any]) -> DeviceResponse:
    device_info = devices_config.devices.from_mac(device['mac'])
    return DeviceResponse(
        last_online=device['scan_time'],
        ip=device['entity']['ip'],
        hostname=device['entity']['hostname'],
        vendor=device['entity']['vendor'],
        open_ports=_get_ports_with_service_names(device['entity']['open_ports']),
        **(device_info.dict())
    )


@router.get('/ip/{ip}', response_model=DeviceResponse)
async def get_ip(ip: str):
    device = scans_data.get_device_by_ip(ip)
    if device is None:
        raise HTTPException(status_code=404, detail='Device not found')
    return _get_device_response(device)


@router.get('/mac/{mac}', response_model=DeviceResponse)
async def get_mac(mac: str):
    device = scans_data.get_device_by_mac(mac)
    if device is None:
        raise HTTPException(status_code=404, detail='Device not found')
    return _get_device_response(device)


@router.get('/name/{name}', response_model=DeviceResponse)
async def get_name(name: str):
    try:
        device = devices_config.devices[name]
    except KeyError:
        raise HTTPException(status_code=404, detail='Device not found')
    return get_mac(device.mac)


@router.get('/all', response_model=DevicesResponse)
async def get_devices():
    devices = scans_data.get_devices()
    return [_get_device_response(device) for device in devices]


@router.get('/all/history', response_model=HistoryResponse)
async def get_history(time_period: float, time_interval: float):
    from_datetime = datetime.now() - timedelta(seconds=time_period)
    history = scans_data.get_history(from_datetime, time_interval)
    return [{'time': entry['_id'], 'average': entry['avg']} for entry in history]
