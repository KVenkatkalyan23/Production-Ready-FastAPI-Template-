"""Authentication request schemas."""

from __future__ import annotations

from pydantic import Field

from app.schemas.common import DisplayName, NormalizedEmail, RequestSchema, StrongPassword


class LoginRequest(RequestSchema):
    """Reusable login payload validation."""

    email: NormalizedEmail
    password: str = Field(..., min_length=1, max_length=255)


class RegisterRequest(RequestSchema):
    """Reusable registration payload validation."""

    email: NormalizedEmail
    password: StrongPassword
    full_name: DisplayName
