from datetime import timedelta, datetime

from jose import jwt, JWTError
from passlib.context import CryptContext

from moonlan.authentication.base_user_provider import BaseUserProvider
from moonlan.authentication.exceptions import AuthenticationError
from moonlan.authentication.models.internal_user import InternalUser
from moonlan.authentication.models.token_data import TokenData
from moonlan.config import config


class AuthenticationManager:
    def __init__(self, user_provider: BaseUserProvider):
        self._user_provider = user_provider
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str):
        try:
            return self._pwd_context.verify(plain_password, hashed_password)
        except ValueError:
            return False

    def get_password_hash(self, password: str):
        try:
            return self._pwd_context.hash(password)
        except ValueError:
            return False

    def authenticate_user(self, email: str, password: str):
        user = self._user_provider.get_user(email)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.authentication.secret_key, algorithm=config.authentication.algorithm)
        return encoded_jwt

    def get_current_user(self, token: str):
        credentials_exception = AuthenticationError("Could not validate credentials")
        try:
            payload = jwt.decode(token, config.authentication.secret_key, algorithms=[config.authentication.algorithm])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        user = self._user_provider.get_user(email=token_data.email)
        if user is None:
            raise credentials_exception
        return user

    def get_current_active_user(self, token: str):
        current_user = self.get_current_user(token)
        if current_user.disabled:
            raise AuthenticationError("Inactive user")
        return current_user

    def login_for_access_token(self, email: str, password: str):
        user = self.authenticate_user(email, password)
        if not user:
            raise AuthenticationError("Incorrect email or password")
        access_token_expires = timedelta(minutes=config.authentication.access_token_expire_minutes)
        access_token = self.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def create_user(self, full_name: str, email: str, password: str):
        user = self._user_provider.get_user(email)
        if user:
            raise AuthenticationError("User already exists")
        self._user_provider.insert_user(InternalUser(
            full_name=full_name,
            email=email,
            hashed_password=self.get_password_hash(password),
            disabled=True,
        ))
        access_token_expires = timedelta(minutes=config.authentication.access_token_expire_minutes)
        access_token = self.create_access_token(data={"sub": email}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
