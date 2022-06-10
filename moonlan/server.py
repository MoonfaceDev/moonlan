import fastapi
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from moonlan import consts
from moonlan.config import config
from moonlan.routers import api

app = fastapi.FastAPI()
app.include_router(api.router)

app.mount('/static', StaticFiles(directory=str(consts.Server.FRONTEND_STATIC_PATH)))
templates = Jinja2Templates(directory=str(consts.Server.FRONTEND_PATH))


@app.get('/{full_path:path}', tags=['Frontend'])
async def get_app(request: Request, full_path: str) -> Response:
    return templates.TemplateResponse(
        consts.Server.FRONTEND_INDEX_FILE_NAME,
        {consts.Server.TEMPLATE_REQUEST_KEY: request}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.server.allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
