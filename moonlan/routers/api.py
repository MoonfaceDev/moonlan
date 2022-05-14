from fastapi import APIRouter

from moonlan.routers import auth, device, spoof

router = APIRouter(prefix='/api')

router.include_router(auth.router)
router.include_router(device.router)
router.include_router(spoof.router)
