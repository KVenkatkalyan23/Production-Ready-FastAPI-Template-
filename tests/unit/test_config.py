"""Tests for environment-based application settings."""

from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from app.core.config import ACTIVE_ENVIRONMENT, ACTIVE_ENV_FILE, Settings, settings


def test_settings_use_testing_environment_file() -> None:
    """The test suite should load the dedicated testing environment."""

    assert ACTIVE_ENVIRONMENT == "testing"
    assert ACTIVE_ENV_FILE.name == ".env.testing"
    assert settings.ENVIRONMENT == "testing"


def test_settings_normalize_cors_origins() -> None:
    """Configured origins should be trimmed consistently."""

    loaded = Settings(
        APP_NAME="Example",
        ENVIRONMENT="testing",
        DEBUG=True,
        DATABASE_URL="sqlite:///./testing.db",
        JWT_SECRET_KEY="secret",
        JWT_ALGORITHM="HS256",
        ACCESS_TOKEN_EXPIRE_MINUTES=5,
        CORS_ORIGINS=[" https://example.com ", "http://localhost:3000 "],
        LOG_LEVEL="INFO",
        LOG_JSON=False,
    )

    assert loaded.CORS_ORIGINS == ["https://example.com", "http://localhost:3000"]


def test_settings_require_secret_configuration() -> None:
    """Settings validation should fail when required security config is missing."""

    try:
        Settings(
            APP_NAME="Example",
            ENVIRONMENT="testing",
            DEBUG=True,
            DATABASE_URL="sqlite:///./testing.db",
            JWT_ALGORITHM="HS256",
            ACCESS_TOKEN_EXPIRE_MINUTES=5,
            CORS_ORIGINS=["http://localhost:3000"],
            LOG_LEVEL="INFO",
            LOG_JSON=False,
            _env_file=None,
        )
    except ValidationError as exc:
        assert "JWT_SECRET_KEY" in str(exc)
    else:
        raise AssertionError("Expected missing secret configuration to fail validation.")


def test_settings_expose_selected_env_file_path() -> None:
    """Settings should report the active env file for diagnostics."""

    assert Path(settings.env_file).name == ".env.testing"
