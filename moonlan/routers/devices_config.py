import json
from json import JSONDecodeError

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from starlette import status
from starlette.responses import Response

from moonlan import consts
from moonlan.dal import devices_dal
from moonlan.dependencies.authentication_dependency import current_active_user
from moonlan.devices.device_manager import devices_config
from moonlan.devices.devices import Devices, DeviceEntry
from moonlan.models.requests.devices_config_update_request import DevicesConfigUpdateRequest
from moonlan.models.responses.devices_config_count_response import DevicesConfigCountResponse

router = APIRouter(prefix='/devices_config', tags=['Devices Config'], dependencies=[Depends(current_active_user)])


@router.get('/count', response_model=DevicesConfigCountResponse)
async def get_count():
    all_devices = devices_dal.get_devices()
    count = 0
    for device in all_devices:
        if devices_config.devices.from_mac(device.entity.mac).name != consts.DeviceManager.DEFAULT_NAME:
            count += 1
    return DevicesConfigCountResponse(count=count)


@router.get('/view')
async def get_file():
    with consts.DeviceManager.DEVICES_CONFIG_PATH.open('r') as file:
        return Response(file.read(), media_type=consts.DeviceManager.VIEW_FILE_CONTENT_TYPE)


@router.post('/update')
async def update_file(request: DevicesConfigUpdateRequest):
    try:
        _assert_devices_config_data(request.data)
    except DevicesConfigValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    with consts.DeviceManager.DEVICES_CONFIG_PATH.open('w') as file:
        file.write(request.data)


def _assert_devices_config_data(data: str):
    try:
        devices = json.loads(data)
    except JSONDecodeError:
        raise DevicesConfigValidationError('Bad JSON format')
    if not isinstance(devices, list):
        raise DevicesConfigValidationError('JSON root is expected to be a list')
    try:
        Devices([DeviceEntry(**device) for device in devices])
    except ValidationError as e:
        raise DevicesConfigValidationError(e)


class DevicesConfigValidationError(ValueError):
    pass
