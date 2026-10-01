from __future__ import annotations

import os
from typing import Any


class AppConfig:
    APP_NAME = os.getenv("APP_NAME", "FastFood POS + Bookkeeping API")
    VERSION = os.getenv("APP_VERSION", "0.1.0")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/fastfood_pos",
    )
    SECRET_KEY = os.getenv("SECRET_KEY", "replace-with-a-long-secure-secret")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    NEXT_PUBLIC_API_URL = os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:8000")


settings = AppConfig()
