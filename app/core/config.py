"""Dynamic environment-based application configuration."""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
ROOT_ENV_FILE = BASE_DIR / ".env"


def _read_environment_from_root_env() -> str | None:
    """Read ENVIRONMENT from the root .env file if it exists."""

    if not ROOT_ENV_FILE.exists():
        return None

    for raw_line in ROOT_ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == "ENVIRONMENT":
            return value.strip().strip("'\"")
    return None


def detect_environment() -> str:
    """Determine the active environment without hardcoded environment names."""

    environment = os.getenv("ENVIRONMENT") or _read_environment_from_root_env() or "development"
    return environment.strip().lower()


ACTIVE_ENVIRONMENT = detect_environment()
ACTIVE_ENV_FILE = BASE_DIR / f".env.{ACTIVE_ENVIRONMENT}"


class Settings(BaseSettings):
    """Application settings loaded from the selected environment file."""

    model_config = SettingsConfigDict(
        env_file=str(ACTIVE_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str
    ENVIRONMENT: str = Field(default=ACTIVE_ENVIRONMENT)
    DEBUG: bool
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    CORS_ORIGINS: list[str]
    LOG_LEVEL: str
    LOG_JSON: bool

    @field_validator("ENVIRONMENT", mode="before")
    @classmethod
    def normalize_environment(cls, value: object) -> str:
        """Normalize the environment name for consistent logging and file selection."""

        if value is None:
            return ACTIVE_ENVIRONMENT
        return str(value).strip().lower()

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def normalize_cors_origins(cls, value: object) -> object:
        """Normalize configured CORS origins by trimming whitespace."""

        if isinstance(value, list):
            return [str(origin).strip() for origin in value]
        return value

    @property
    def env_file(self) -> str:
        """Expose the selected environment file for startup diagnostics."""

        return str(ACTIVE_ENV_FILE)


settings = Settings()
