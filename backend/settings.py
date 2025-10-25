"""Application settings loaded from environment variables."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the backend services."""

    model_config = SettingsConfigDict(env_prefix="API_", env_file=".env", extra="ignore")

    environment: str = "dev"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 30
    allowed_origins: List[str] = ["*"]
    alpaca_base_url: str = "https://paper-api.alpaca.markets"
    iex_base_url: str = "https://cloud.iexapis.com/v1"
    iex_token: str | None = None
    redis_url: str = "redis://localhost:6379/0"
    ray_status: str = "stopped"
    data_root: str = "data"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached instance of the application settings."""

    return Settings()
