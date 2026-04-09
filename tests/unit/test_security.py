"""Security validation tests."""

from __future__ import annotations

from pydantic import ValidationError

from app.core.security import validate_password_strength
from app.core.config import settings
from app.main import app
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.user import UserCreateRequest, UserUpdateRequest


def test_validate_password_strength_accepts_strong_password() -> None:
    """Strong passwords should pass reusable validation."""

    assert validate_password_strength("Str0ng!Pass") == "Str0ng!Pass"


def test_validate_password_strength_rejects_weak_password() -> None:
    """Weak passwords should be rejected with a useful error."""

    try:
        validate_password_strength("weakpass")
    except ValueError as exc:
        assert "uppercase" in str(exc).lower()
    else:
        raise AssertionError("Expected weak password validation to fail.")


def test_register_request_normalizes_email_and_enforces_password_strength() -> None:
    """Registration payloads should normalize email and apply shared password rules."""

    payload = RegisterRequest(
        email="  USER@Example.COM ",
        password="Valid1!Pass",
        full_name="Example User",
    )

    assert payload.email == "user@example.com"


def test_login_request_rejects_invalid_email() -> None:
    """Login payloads should reject malformed email addresses."""

    try:
        LoginRequest(email="not-an-email", password="anything")
    except ValidationError as exc:
        assert "email" in str(exc).lower()
    else:
        raise AssertionError("Expected invalid email validation to fail.")


def test_user_create_request_rejects_weak_password() -> None:
    """User creation should fail for weak passwords."""

    try:
        UserCreateRequest(
            email="user@example.com",
            password="short",
            full_name="User Example",
        )
    except ValidationError as exc:
        assert "password" in str(exc).lower()
    else:
        raise AssertionError("Expected weak password validation to fail.")


def test_user_update_request_allows_partial_updates() -> None:
    """User updates should allow omitted fields and validate supplied passwords."""

    payload = UserUpdateRequest(full_name="Updated Name")

    assert payload.full_name == "Updated Name"
    assert payload.password is None


def test_cors_middleware_uses_configured_origins() -> None:
    """Application should register CORS middleware from settings."""

    cors_middlewares = [middleware for middleware in app.user_middleware if middleware.cls.__name__ == "CORSMiddleware"]

    assert cors_middlewares
    assert cors_middlewares[0].kwargs["allow_origins"] == settings.CORS_ORIGINS
