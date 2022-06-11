import json

from fastapi import APIRouter, Depends

from moonlan import consts
from moonlan.dal import scans_dal
from moonlan.dependencies.authentication_dependency import current_active_user
from moonlan.models.responses.scan_info_interval_response import ScanInfoIntervalResponse
from moonlan.models.responses.scan_info_last_scan_response import ScanInfoLastScanResponse

router = APIRouter(prefix='/scan_info', tags=['Scan Info'], dependencies=[Depends(current_active_user)])


@router.get('/last_scan', response_model=ScanInfoLastScanResponse)
async def get_last_scan():
    return ScanInfoLastScanResponse(last_scan=scans_dal.get_last_scan_time().scan_time)


@router.get('/interval', response_model=ScanInfoIntervalResponse)
async def get_interval():
    with consts.Settings.SCAN_CONFIG_PATH.open('r') as file:
        scan_config = json.load(file)
        return ScanInfoIntervalResponse(
            interval=scan_config['network_scan']['scan_interval']
        )
