"""Integration tests for application health endpoints."""

from __future__ import annotations

import pytest

from app.core.config import settings


@pytest.mark.integration
def test_health_check_returns_success_response(client) -> None:
    """Health endpoint should return the shared success envelope."""

    response = client.get("/health")

    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["message"] == "Request completed successfully"
    assert body["data"]["status"] == "healthy"
    assert body["data"]["environment"] == settings.ENVIRONMENT


@pytest.mark.integration
def test_health_check_exposes_testing_environment(client) -> None:
    """Test suite should boot the application with testing settings."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["data"]["environment"] == "testing"
