from fastapi import APIRouter, HTTPException, Depends

from moonlan.authentication_api import current_active_user
from moonlan.models.responses.spoofed_device_response import SpoofedDeviceResponse
from moonlan.spoofing.exceptions import AlreadySpoofingError
from moonlan.spoofing.spoofing_manager import SpoofingManager

spoofing_manager = SpoofingManager()

router = APIRouter(prefix='/spoof', tags=['Spoofing'], dependencies=[Depends(current_active_user)])


@router.get('/device', response_model=SpoofedDeviceResponse)
async def get_spoofed_device():
    return spoofing_manager.spoofed_device


@router.post('/start')
async def post_start_spoof(ip: str, mac: str, forward: bool):
    try:
        spoofing_manager.start_spoof(ip, mac, forward)
    except AlreadySpoofingError:
        raise HTTPException(status_code=403, detail='Already spoofing')


@router.post('/stop')
async def post_stop_spoof():
    spoofing_manager.stop_spoof()
