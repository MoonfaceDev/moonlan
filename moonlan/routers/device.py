from _socket import getservbyport
from datetime import datetime, timedelta

import numpy
from fastapi import APIRouter, Depends, HTTPException

from moonlan.dal import scans_dal, devices_dal
from moonlan.dal.documents.device_document import DeviceDocument
from moonlan.dal.documents.device_scan_document import DeviceScanDocument
from moonlan.dependencies.authentication_dependency import current_active_user
from moonlan.devices.device_manager import devices_config
from moonlan.models.responses.device_response import DeviceResponse
from moonlan.models.responses.devices_response import DevicesResponse
from moonlan.models.responses.history_response import HistoryResponse
from moonlan.models.responses.uptime_history_response import UptimeHistoryResponse

router = APIRouter(prefix='/device', tags=['Devices'], dependencies=[Depends(current_active_user)])


def _get_ports_with_service_names(ports: list[int]) -> list[dict]:
    def safe_get_service_name(port: int) -> str:
        try:
            return getservbyport(port, "tcp")
        except OSError:
            return ''

    return [{'port': port, 'service': safe_get_service_name(port)} for port in ports]


def _get_device_response(document: DeviceDocument) -> DeviceResponse:
    device_info = devices_config.devices.from_mac(document.entity.mac)
    return DeviceResponse(
        last_online=document.scan_time,
        ip=document.entity.ip,
        hostname=document.entity.hostname,
        vendor=document.entity.vendor,
        open_ports=_get_ports_with_service_names(document.entity.open_ports),
        **(device_info.dict())
    )


@router.get('/ip/{ip}', response_model=DeviceResponse)
async def get_ip(ip: str):
    device = devices_dal.get_device_by_ip(ip)
    if device is None:
        raise HTTPException(status_code=404, detail='Device not found')
    return _get_device_response(device)


@router.get('/mac/{mac}', response_model=DeviceResponse)
async def get_mac(mac: str):
    device = devices_dal.get_device_by_mac(mac)
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
    devices = devices_dal.get_devices()
    return [_get_device_response(device) for device in devices]


@router.get('/all/history', response_model=HistoryResponse)
async def get_history(start_timestamp: float, end_timestamp: float, time_interval: float):
    start_datetime = datetime.fromtimestamp(start_timestamp)
    end_datetime = datetime.fromtimestamp(end_timestamp)
    history = scans_dal.get_history(start_datetime, end_datetime, time_interval)
    return [{'time': entry.id, 'average': entry.avg} for entry in history]


@router.get('/mac/{mac}/uptime', response_model=UptimeHistoryResponse)
async def get_uptime_history(mac: str, start_timestamp: float, end_timestamp: float, time_interval: float):
    start_datetime = datetime.fromtimestamp(start_timestamp)
    end_datetime = datetime.fromtimestamp(end_timestamp)
    scans = list(scans_dal.get_scans_for_device(mac, start_datetime, end_datetime))
    online_times = _get_online_times(scans, start_datetime)
    return [
        {'time': group_start_time, 'uptime': group_online_time}
        for group_start_time, group_online_time
        in _get_uptime_history_groups(start_datetime, end_datetime, time_interval, online_times)
    ]


def _get_uptime_history_groups(
        start_datetime: datetime,
        end_datetime: datetime,
        time_interval: float,
        online_times: list[tuple[datetime, datetime]]
) -> list[tuple[datetime, timedelta]]:
    uptime_history = []
    for group_start_timestamp in numpy.arange(start_datetime.timestamp(), end_datetime.timestamp(), time_interval):
        group_start_datetime = datetime.fromtimestamp(group_start_timestamp)
        group_end_datetime = min(group_start_datetime + timedelta(seconds=time_interval), end_datetime)
        group_uptime = _get_group_uptime(group_start_datetime, group_end_datetime, online_times)
        uptime_history.append((group_start_datetime, group_uptime))

    return uptime_history


def _get_group_uptime(
        group_start_datetime: datetime,
        group_end_datetime: datetime,
        online_times: list[tuple[datetime, datetime]]
) -> timedelta:
    uptime = 0
    for time_range in online_times:
        intersection_start = max(group_start_datetime.timestamp(), time_range[0].timestamp())
        intersection_end = min(group_end_datetime.timestamp(), time_range[1].timestamp())
        intersection_duration = intersection_end - intersection_start
        if intersection_duration > 0:
            uptime += intersection_duration
    return timedelta(seconds=uptime)


def _get_online_times(scans: list[DeviceScanDocument], start_datetime: datetime) -> list[tuple[datetime, datetime]]:
    online_times = []
    if not scans:
        return online_times

    if scans[0].online:
        online_times.append((start_datetime, scans[0].scan_time))

    for i in range(1, len(scans)):
        if scans[i].online:
            online_times.append((scans[i - 1].scan_time, scans[i].scan_time))

    return online_times
