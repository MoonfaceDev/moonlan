from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from moonlan.authentication.authentication_manager import AuthenticationManager
from moonlan.authentication.database_user_provider import DatabaseUserProvider
from moonlan.authentication.exceptions import AuthenticationError
from moonlan.config import config

authentication_manager = AuthenticationManager(DatabaseUserProvider(config.database.database_name))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def current_active_user(token: str = Depends(oauth2_scheme)):
    try:
        return authentication_manager.get_current_active_user(token)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
