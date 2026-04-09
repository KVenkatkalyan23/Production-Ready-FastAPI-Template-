"""Success response schema."""

from typing import Any

from pydantic import Field

from app.schemas.base import BaseResponse


class SuccessResponse(BaseResponse):
    """Reusable success response envelope."""

    success: bool = Field(default=True, description="Indicates a successful response.")
    data: Any | None = Field(default=None, description="Payload returned by the endpoint.")
