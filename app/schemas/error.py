"""Error response schema."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base import BaseResponse


class ErrorDetail(BaseModel):
    """Structured error metadata for failed API responses."""

    model_config = ConfigDict(extra="forbid")

    code: str = Field(..., description="Stable application-level error code.")
    details: Any | None = Field(
        default=None,
        description="Optional structured context for the error.",
    )


class ErrorResponse(BaseResponse):
    """Reusable error response envelope."""

    success: bool = Field(default=False, description="Indicates a failed response.")
    error: ErrorDetail = Field(..., description="Structured error information.")
