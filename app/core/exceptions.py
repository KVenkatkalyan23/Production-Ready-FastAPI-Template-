"""Reusable application exception types."""

from __future__ import annotations


class AppException(Exception):
    """Base exception for expected application errors."""

    def __init__(
        self,
        message: str,
        *,
        error_code: str = "APP_ERROR",
        status_code: int = 400,
        details: dict[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}


class BadRequestException(AppException):
    """400 bad request exception."""

    def __init__(self, message: str = "Bad request", *, details: dict[str, object] | None = None) -> None:
        super().__init__(message, error_code="BAD_REQUEST", status_code=400, details=details)


class UnauthorizedException(AppException):
    """401 unauthorized exception."""

    def __init__(self, message: str = "Unauthorized", *, details: dict[str, object] | None = None) -> None:
        super().__init__(message, error_code="UNAUTHORIZED", status_code=401, details=details)


class ForbiddenException(AppException):
    """403 forbidden exception."""

    def __init__(self, message: str = "Forbidden", *, details: dict[str, object] | None = None) -> None:
        super().__init__(message, error_code="FORBIDDEN", status_code=403, details=details)


class NotFoundException(AppException):
    """404 not found exception."""

    def __init__(self, message: str = "Resource not found", *, details: dict[str, object] | None = None) -> None:
        super().__init__(message, error_code="NOT_FOUND", status_code=404, details=details)


class ConflictException(AppException):
    """409 conflict exception."""

    def __init__(self, message: str = "Conflict", *, details: dict[str, object] | None = None) -> None:
        super().__init__(message, error_code="CONFLICT", status_code=409, details=details)
