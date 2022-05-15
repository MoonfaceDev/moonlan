from fastapi import APIRouter, Depends, Form, HTTPException
from starlette import status

from moonlan.authentication_api import current_active_user, authentication_manager
from moonlan.authentication.exceptions import AuthenticationError
from moonlan.models.responses.token_response import TokenResponse
from moonlan.models.user import User

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.get('/check_token')
async def check_token(current_user: User = Depends(current_active_user)):
    return ''


@router.post("/login", response_model=TokenResponse)
async def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    try:
        return authentication_manager.login_for_access_token(username, password)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register", response_model=TokenResponse)
async def register_for_access_token(full_name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        return authentication_manager.create_user(full_name, email, password)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
