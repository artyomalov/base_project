from time import time
from .jwt_actions_util import jwt_actions_util

from config import settings


class JWTCreatorUtil:
    def __init__(
        self,
        username: str,
        access_token_expire_time: int,
        refresh_token_expire_time: int,
        # is_admin: bool,
    ):
        self.username = username
        self.access_token_expire_time = access_token_expire_time
        self.refresh_token_expire_time = refresh_token_expire_time
        # self.is_admin = is_admin

    def create_access_token(self) -> bytes:
        timestamp = int(time())
        payload = {
            "sub": self.username,
            "token_type": settings.auth_jwt.ACCESS_TOKEN_TYPE,
            "iat": timestamp,
            "exp": timestamp + self.access_token_expire_time,
        }

        return jwt_actions_util.encode_jwt(payload)

    def create_refresh_token(self) -> bytes:
        timestamp = int(time())
        payload = {
            "sub": self.username,
            "token_type": settings.auth_jwt.REFRESH_TOKEN_TYPE,
            "iat": timestamp,
            "exp": timestamp + self.refresh_token_expire_time,
        }

        return jwt_actions_util.encode_jwt(payload)
