"""Base API response schema primitives."""

from pydantic import BaseModel, ConfigDict, Field


class BaseResponse(BaseModel):
    """Shared response envelope for all API responses."""

    model_config = ConfigDict(extra="forbid")

    success: bool = Field(..., description="Whether the request completed successfully.")
    message: str = Field(..., description="Human-readable summary of the response.")
