"""Authentication request schemas."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.core.security import validate_password_strength


class LoginRequest(BaseModel):
    """Reusable login payload validation."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    email: EmailStr
    password: str = Field(..., min_length=1, max_length=255)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: object) -> str:
        """Normalize emails for consistent lookup behavior."""

        return str(value).strip().lower()


class RegisterRequest(BaseModel):
    """Reusable registration payload validation."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)
    full_name: str = Field(..., min_length=1, max_length=255)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: object) -> str:
        """Normalize emails for consistent persistence."""

        return str(value).strip().lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Enforce reusable password strength rules."""

        return validate_password_strength(value)
