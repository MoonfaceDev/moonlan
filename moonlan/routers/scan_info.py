import json

from fastapi import APIRouter, Depends
from starlette.responses import Response

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
    with consts.ScanInfo.SCAN_CONFIG_PATH.open('r') as file:
        scan_config = json.load(file)
        return ScanInfoIntervalResponse(
            interval=scan_config[consts.ScanInfo.NETWORK_SCAN_KEY][consts.ScanInfo.SCAN_INTERVAL_KEY]
        )


@router.get('/view')
async def get_file():
    with consts.ScanInfo.SCAN_CONFIG_PATH.open('r') as file:
        return Response(file.read(), media_type=consts.ScanInfo.VIEW_FILE_CONTENT_TYPE)


@router.post('/update')
async def update_file(data: str):
    with consts.ScanInfo.SCAN_CONFIG_PATH.open('w') as file:
        file.write(data)
