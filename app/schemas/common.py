"""Reusable schema building blocks."""

from __future__ import annotations

from typing import Annotated

from pydantic import AfterValidator, BaseModel, BeforeValidator, ConfigDict, EmailStr, Field

from app.core.security import normalize_email, validate_password_strength


class RequestSchema(BaseModel):
    """Base model for request payload validation."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


NormalizedEmail = Annotated[EmailStr, BeforeValidator(normalize_email)]
StrongPassword = Annotated[
    str,
    Field(min_length=8, max_length=255),
    AfterValidator(validate_password_strength),
]
OptionalStrongPassword = Annotated[
    str | None,
    Field(default=None, min_length=8, max_length=255),
    AfterValidator(lambda value: value if value is None else validate_password_strength(value)),
]
DisplayName = Annotated[str, Field(min_length=1, max_length=255)]
