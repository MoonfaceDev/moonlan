from pathlib import Path

import fastapi
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from moonlan.config import config
from moonlan.routers import api

app = fastapi.FastAPI()
app.include_router(api.router)

app.mount('/static', StaticFiles(directory='/etc/moonitor/app/static'))
templates = Jinja2Templates(directory=str(Path("/etc/moonitor/app").expanduser()))


@app.get('/{full_path:path}', tags=['Frontend'])
async def get_app(request: Request, full_path: str) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.server.allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
