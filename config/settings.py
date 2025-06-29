import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from datetime import datetime, UTC, timedelta


BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    PRIVATE_KEY_PATH: Path = BASE_DIR / "config" / "certs" / "jwt-private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "config" / "certs" / "jwt-public.pem"
    ALGORITHM: str = "RS256"

    ACCESS_TOKEN_TYPE: str = "access"
    REFRESH_TOKEN_TYPE: str = "refresh"

    REFRESH_TOKEN_EXPIRE_TIME: int = 3000
    ACCESS_TOKEN_EXPIRE_TIME: int = 86400
    # REFRESH_TOKEN_EXPIRE_TIME: datetime = datetime.now(UTC) + timedelta(minutes=20)
    # ACCESS_TOKEN_EXPIRE_TIME: datetime = datetime.now(UTC) + timedelta(minutes=5)

    ALLOW_ANY_ROUTES: list[str] = (
        "/api/v1/auth/login",
        "/api/v1/auth/refresh",
        "/api/v1/healthcheck",
        "/docs",
        "/favicon.ico",
        "/openapi.json",
    )

    ADMIN_ROUTES: list[str] = (
        "/api/v1/user/get-users-previews-list-and-positions-list",
        "/api/v1/user/create",
        "/api/v1/user/update-user-data-by-admin/{username}",
        "/api/v1/user/delete/{deleted_username}",
        "/api/v1/position/all",
        "/api/v1/position/create",
        "/api/v1/position/update/{position_id}",
        "/api/v1/position/update/{position_id}",
    )


class Setting(BaseSettings):
    # class Setting:
    PRODUCTION: bool = False
    DOKERIZED: bool = False
    TESTING: bool = False

    DEVELOPMENT_BASE_URL: str = "http://0.0.0.0"
    PRODUCTION_BASE_URL: str = "https://production.com"
    BASE_URL: str = DEVELOPMENT_BASE_URL if not PRODUCTION else PRODUCTION_BASE_URL

    MEDIA_ROOT: Path = BASE_DIR / " media"
    # MEDIA_ROOT: Path = BASE_DIR / "files" / "media"
    # private_key_path: Path = (
    #     BASE_DIR / "files" / "apps" / "user_auth" / "certs" / "jwt-private.pem"
    # )
    BASE_LOG_DIR: Path = BASE_DIR / "logs"
    # BASE_LOG_DIR: str = "E:\propgram\mp_search_crm\server"

    IMAGE_AVATAR_TYPE: str = "avatar"

    LOG_EVENT_LIFE_PERIOD: timedelta = timedelta(days=7)

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_NAME: str = None

    auth_jwt: AuthJWT = AuthJWT()
    REQUIRE_AUTH: bool = False

    API_VERSION: str = "v1"
    BASE_URL = "localhost:8000/api" + "/" + API_VERSION

    @property
    def database_url(self):
        if self.TESTING:
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.TEST_DB_NAME}"

        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}"

    model_config = (
        SettingsConfigDict(
            extra="allow",
            env_file=os.path.abspath(os.path.join(BASE_DIR, ".env_local")),
        )
        if not DOKERIZED
        else SettingsConfigDict(
            extra="allow",
            env_file=os.path.abspath(os.path.join(BASE_DIR, ".env_docker")),
        )
    )


settings = Setting()
