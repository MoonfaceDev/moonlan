from datetime import datetime, timedelta
from pathlib import Path

import fastapi
from fastapi import HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from moonlan.authentication.authentication_manager import AuthenticationManager
from moonlan.authentication.database_user_provider import DatabaseUserProvider
from moonlan.authentication.exceptions import AuthenticationError
from moonlan.authentication.models.token import Token
from moonlan.authentication.models.user import User
from moonlan.config import config
from moonlan.exceptions import DeviceNotFoundError
from moonlan.scans_data import ScansData
from moonlan.spoofing.exceptions import AlreadySpoofingError
from moonlan.spoofing.spoofing_manager import SpoofingManager

app = fastapi.FastAPI()

app.mount('/static', StaticFiles(directory='/etc/moonitor/app/static'))
templates = Jinja2Templates(directory=str(Path("/etc/moonitor/app").expanduser()))

scans_data = ScansData(config.database.database_name)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
authentication_manager = AuthenticationManager(DatabaseUserProvider(config.database.database_name))
spoofing_manager = SpoofingManager()


async def current_active_user(token: str = Depends(oauth2_scheme)):
    try:
        return authentication_manager.get_current_active_user(token)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get('/check_token')
async def check_token(current_user: User = Depends(current_active_user)):
    return ''


@app.post("/login/token", response_model=Token)
async def login_for_access_token(email: str = Form(...), password: str = Form(...)):
    try:
        return authentication_manager.login_for_access_token(email, password)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/register/token", response_model=Token)
async def register_for_access_token(full_name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        return authentication_manager.create_user(full_name, email, password)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get('/last')
async def get_last(current_user: User = Depends(current_active_user)):
    return scans_data.get_last()


@app.get('/ip/{ip}')
async def get_ip(ip: str, current_user: User = Depends(current_active_user)):
    try:
        return scans_data.get_ip(ip)
    except DeviceNotFoundError:
        raise HTTPException(status_code=404, detail='Device not found')


@app.get('/device/{name}')
async def get_device(name: str, current_user: User = Depends(current_active_user)):
    try:
        return scans_data.get_device(name)
    except DeviceNotFoundError:
        raise HTTPException(status_code=404, detail='Device not found')


@app.get('/history')
async def get_history(time_period: float, time_interval: float, current_user: User = Depends(current_active_user)):
    from_datetime = datetime.now() - timedelta(seconds=time_period)
    return scans_data.get_history(from_datetime, time_interval)


@app.get('/devices')
async def get_devices():
    return scans_data.get_devices()


@app.get('/spoofed_device')
async def get_spoofed_device():
    return spoofing_manager.spoofed_device


@app.post('/spoof/start')
async def post_start_spoof(ip: str, mac: str, forward: bool, current_user: User = Depends(current_active_user)):
    try:
        spoofing_manager.start_spoof(ip, mac, forward)
    except AlreadySpoofingError:
        raise HTTPException(status_code=403, detail='Already spoofing')


@app.post('/spoof/stop')
async def post_stop_spoof():
    spoofing_manager.stop_spoof()


@app.get('/{full_path:path}')
async def get_app(request: Request, full_path: str) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.server.allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
