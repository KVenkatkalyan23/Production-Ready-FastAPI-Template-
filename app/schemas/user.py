"""User request schemas."""

from __future__ import annotations

from app.schemas.common import (
    DisplayName,
    NormalizedEmail,
    OptionalStrongPassword,
    RequestSchema,
    StrongPassword,
)


class UserCreateRequest(RequestSchema):
    """Reusable user creation payload validation."""

    email: NormalizedEmail
    password: StrongPassword
    full_name: DisplayName


class UserUpdateRequest(RequestSchema):
    """Reusable user update payload validation."""

    full_name: DisplayName | None = None
    password: OptionalStrongPassword = None
