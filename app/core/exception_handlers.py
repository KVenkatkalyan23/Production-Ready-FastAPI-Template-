"""Centralized FastAPI exception handling."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.schemas.error import ErrorDetail, ErrorResponse


logger = logging.getLogger(__name__)


def _error_response(*, status_code: int, message: str, code: str, details: Any = None) -> JSONResponse:
    """Build the standard API error response envelope."""

    response = ErrorResponse(
        message=message,
        error=ErrorDetail(code=code, details=details),
    )
    return JSONResponse(status_code=status_code, content=response.model_dump())


async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    """Handle expected application exceptions."""

    logger.warning(
        "Application exception",
        extra={"error_code": exc.error_code, "details": exc.details},
    )
    return _error_response(
        status_code=exc.status_code,
        message=exc.message,
        code=exc.error_code,
        details=exc.details,
    )


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI/Starlette HTTP exceptions."""

    details = exc.detail if isinstance(exc.detail, (dict, list)) else None
    message = exc.detail if isinstance(exc.detail, str) else "HTTP request failed"
    logger.warning(
        "HTTP exception",
        extra={"error_code": "HTTP_EXCEPTION", "details": details or exc.detail},
    )
    return _error_response(
        status_code=exc.status_code,
        message=message,
        code="HTTP_EXCEPTION",
        details=details,
    )


async def request_validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation failures with a consistent envelope."""

    details = {"errors": exc.errors()}
    logger.warning(
        "Request validation failed",
        extra={"error_code": "VALIDATION_ERROR", "details": details},
    )
    return _error_response(
        status_code=422,
        message="Request validation failed",
        code="VALIDATION_ERROR",
        details=details,
    )


async def unexpected_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected errors without exposing internal details."""

    logger.exception(
        "Unhandled exception",
        extra={"error_code": "INTERNAL_SERVER_ERROR", "details": {}},
        exc_info=exc,
    )
    return _error_response(
        status_code=500,
        message="Internal server error",
        code="INTERNAL_SERVER_ERROR",
        details={},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all application-wide exception handlers."""

    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(Exception, unexpected_exception_handler)
