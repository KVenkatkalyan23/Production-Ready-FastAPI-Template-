"""Reusable API response schemas."""

from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.base import BaseResponse
from app.schemas.common import RequestSchema
from app.schemas.error import ErrorDetail, ErrorResponse
from app.schemas.success import SuccessResponse
from app.schemas.user import UserCreateRequest, UserUpdateRequest

__all__ = [
    "BaseResponse",
    "ErrorDetail",
    "ErrorResponse",
    "LoginRequest",
    "RequestSchema",
    "RegisterRequest",
    "SuccessResponse",
    "UserCreateRequest",
    "UserUpdateRequest",
]
