"""Tests for centralized exception handling and logging contracts."""

from __future__ import annotations

import io
import json
import logging

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
import pytest
from starlette.requests import Request

from app.core.exception_handlers import (
    app_exception_handler,
    http_exception_handler,
    request_validation_exception_handler,
    unexpected_exception_handler,
)
from app.core.exceptions import ConflictException
from app.core.logging import JsonFormatter


def _build_request() -> Request:
    """Create a minimal ASGI request for handler tests."""

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [],
    }
    return Request(scope)


@pytest.mark.asyncio
async def test_app_exception_handler_returns_standard_response() -> None:
    """Custom application exceptions should map to the standard envelope."""

    response = await app_exception_handler(
        _build_request(),
        ConflictException("User already exists", details={"email": "user@example.com"}),
    )

    body = json.loads(response.body)

    assert response.status_code == 409
    assert body["success"] is False
    assert body["message"] == "User already exists"
    assert body["error"]["code"] == "CONFLICT"
    assert body["error"]["details"] == {"email": "user@example.com"}


@pytest.mark.asyncio
async def test_http_exception_handler_returns_standard_response() -> None:
    """HTTP exceptions should be normalized into the shared envelope."""

    response = await http_exception_handler(
        _build_request(),
        HTTPException(status_code=404, detail="Missing route"),
    )

    body = json.loads(response.body)

    assert response.status_code == 404
    assert body["message"] == "Missing route"
    assert body["error"]["code"] == "HTTP_EXCEPTION"


@pytest.mark.asyncio
async def test_request_validation_exception_handler_returns_standard_response() -> None:
    """Validation errors should return a 422 shared envelope."""

    response = await request_validation_exception_handler(
        _build_request(),
        RequestValidationError(
            [
                {
                    "type": "missing",
                    "loc": ("body", "email"),
                    "msg": "Field required",
                    "input": {},
                }
            ]
        ),
    )

    body = json.loads(response.body)

    assert response.status_code == 422
    assert body["message"] == "Request validation failed"
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["details"]["errors"]


@pytest.mark.asyncio
async def test_unexpected_exception_handler_hides_internal_errors() -> None:
    """Unexpected errors should not expose raw internal details."""

    response = await unexpected_exception_handler(_build_request(), RuntimeError("database exploded"))

    body = json.loads(response.body)

    assert response.status_code == 500
    assert body["message"] == "Internal server error"
    assert body["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert body["error"]["details"] == {}


def test_json_formatter_includes_structured_exception_fields() -> None:
    """JSON logging should emit the expected structured keys."""

    logger = logging.getLogger("test.json.formatter")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)
    logger.propagate = False

    logger.error("Failure", extra={"error_code": "APP_ERROR", "details": {"foo": "bar"}})

    payload = json.loads(stream.getvalue())

    assert payload["level"] == "ERROR"
    assert payload["logger"] == "test.json.formatter"
    assert payload["message"] == "Failure"
    assert payload["error_code"] == "APP_ERROR"
    assert payload["details"] == {"foo": "bar"}
