from pydantic import BaseModel


class Settings(BaseModel):
    APP_NAME: str = "FastFood POS + Bookkeeping API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fastfood_pos"
    SECRET_KEY: str = "replace-with-a-long-secure-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings()
