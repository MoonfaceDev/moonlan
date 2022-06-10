import json
from pathlib import Path

from fastapi import APIRouter, Depends
from starlette.responses import Response

from moonlan.dependencies.authentication_dependency import current_active_user
from moonlan.dal import scans_data
from moonlan.models.responses.scan_info_interval_response import ScanInfoIntervalResponse
from moonlan.models.responses.scan_info_last_scan_response import ScanInfoLastScanResponse

SCAN_CONFIG_PATH = Path('/etc/moonitor/scan/config.json')

router = APIRouter(prefix='/scan_info', tags=['Scan Info'], dependencies=[Depends(current_active_user)])


@router.get('/last_scan', response_model=ScanInfoLastScanResponse)
async def get_last_scan():
    return {'last_scan': scans_data.get_last_scan_time().scan_time}


@router.get('/interval', response_model=ScanInfoIntervalResponse)
async def get_interval():
    with SCAN_CONFIG_PATH.open('r') as file:
        scan_config = json.load(file)
        return {'interval': scan_config['network_scan']['scan_interval']}


@router.get('/view')
async def get_file():
    with SCAN_CONFIG_PATH.open('r') as file:
        return Response(file.read(), media_type='application/json')


@router.post('/update')
async def update_file(data: str):
    with SCAN_CONFIG_PATH.open('w') as file:
        file.write(data)
