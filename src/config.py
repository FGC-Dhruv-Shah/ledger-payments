"""Application configuration.

Settings are loaded exclusively from the environment (or a local `.env` file).
No secrets are ever hardcoded in source — `secret_key` has no default and must
be provided by the deployment environment.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="MERIDIAN_",
        extra="ignore",
    )

    environment: str = "development"
    database_path: str = "ledger.db"
    secret_key: str  # required — supplied via MERIDIAN_SECRET_KEY
    log_level: str = "INFO"
    api_title: str = "Meridian Pay — Ledger & Payments API"
    api_version: str = "1.2.0"


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance for the process lifetime."""
    return Settings()
