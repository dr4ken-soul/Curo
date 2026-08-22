"""Runtime settings for the Curo API."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed application settings."""

    fortyguard_api_key: str | None = None
    fortyguard_base_url: str = "https://api.fortyguard.com/v1"
    curo_db_path: str = "./curo.sqlite3"
    curo_poll_seconds: float = 2.0
    curo_poll_attempts: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process settings singleton."""

    return Settings()

