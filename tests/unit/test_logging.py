"""Tests for logging configuration behavior."""

from __future__ import annotations

import io
import json
import logging

from app.core.logging import JsonFormatter, configure_logging


def test_json_formatter_includes_exception_text() -> None:
    """JSON formatter should serialize exception details when present."""

    try:
        raise RuntimeError("boom")
    except RuntimeError:
        record = logging.getLogger("json-test").makeRecord(
            "json-test",
            logging.ERROR,
            __file__,
            10,
            "Failure",
            args=(),
            exc_info=True,
            extra={"error_code": "INTERNAL_SERVER_ERROR", "details": {"stage": "test"}},
        )

    payload = json.loads(JsonFormatter().format(record))

    assert payload["message"] == "Failure"
    assert payload["error_code"] == "INTERNAL_SERVER_ERROR"
    assert payload["details"] == {"stage": "test"}
    assert "exception" in payload


def test_configure_logging_uses_json_formatter_when_enabled() -> None:
    """JSON logging mode should install the custom formatter."""

    configure_logging("INFO", True)

    handler = logging.getLogger().handlers[0]

    assert isinstance(handler.formatter, JsonFormatter)


def test_configure_logging_uses_plain_formatter_when_json_disabled() -> None:
    """Plain logging mode should install a standard formatter."""

    configure_logging("DEBUG", False)

    handler = logging.getLogger().handlers[0]

    assert not isinstance(handler.formatter, JsonFormatter)
    assert logging.getLogger().level == logging.DEBUG


def test_json_logging_handler_emits_parseable_payload() -> None:
    """Configured JSON logging should produce valid JSON output."""

    stream = io.StringIO()
    configure_logging("INFO", True)
    root_logger = logging.getLogger()
    root_logger.handlers[0].stream = stream

    root_logger.info("Startup complete")

    payload = json.loads(stream.getvalue())

    assert payload["level"] == "INFO"
    assert payload["message"] == "Startup complete"
