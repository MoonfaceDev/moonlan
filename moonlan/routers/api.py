from fastapi import APIRouter

from moonlan.routers import auth, device, spoof, devices_config, scan_info

router = APIRouter(prefix='/api')

router.include_router(auth.router)
router.include_router(device.router)
router.include_router(spoof.router)
router.include_router(devices_config.router)
router.include_router(scan_info.router)
