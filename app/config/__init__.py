import os
from typing import List, Optional, cast

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    RDS_URI: str = cast(str, os.getenv("RDS_URI"))
    API_KEY: str = cast(str, os.getenv("API_KEY", "TEST"))
    PORT: int = cast(int, os.getenv("PORT", 8000))
    # The hosts to add as trusted hosts for this API
    TRUSTED_HOSTS: list[str] = ["*"]
    DEV_MODE: bool = cast(bool, os.getenv("DEV_MODE", False))
    SECRET_KEY: str = cast(str, os.getenv("SECRET_KEY", "TEST"))
    ALGORITHM: str = cast(str, os.getenv("ALGORITHM", "HS256"))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = cast(
        int, os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = cast(
        int, os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)
    )
    API_V1_STR: str = cast(str, os.getenv("API_V1_STR", "/api/v1"))
    DOCS_USERNAME: str = cast(str, os.getenv("DOCS_USERNAME", "admin"))
    DOCS_PASSWORD: str = cast(str, os.getenv("DOCS_PASSWORD", "admin"))
    REQUEST_TIMEOUT_SECONDS: int = cast(int, os.getenv("REQUEST_TIMEOUT_SECONDS", 30))

    class Config:
        case_sensitive = False

config = Config()
