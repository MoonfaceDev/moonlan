from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException

from moonlan import scans_data
from moonlan.authentication_api import current_active_user
from moonlan.exceptions import DeviceNotFoundError

router = APIRouter(prefix='/device', tags=['Devices'], dependencies=[Depends(current_active_user)])


@router.get('/ip/{ip}')
async def get_ip(ip: str):
    try:
        return scans_data.get_device_by_ip(ip)
    except DeviceNotFoundError:
        raise HTTPException(status_code=404, detail='Device not found')


@router.get('/name/{name}')
async def get_device(name: str):
    try:
        return scans_data.get_device_by_name(name)
    except DeviceNotFoundError:
        raise HTTPException(status_code=404, detail='Device not found')


@router.get('/all')
async def get_devices():
    return scans_data.get_devices()


@router.get('/history')
async def get_history(time_period: float, time_interval: float):
    from_datetime = datetime.now() - timedelta(seconds=time_period)
    return scans_data.get_history(from_datetime, time_interval)
