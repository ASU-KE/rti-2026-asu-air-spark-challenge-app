"""Integration tests for GET /health, exercised through the HTTP boundary."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    return TestClient(app)


def test_health_returns_success_envelope(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {"status": "ok"},
        "error": None,
        "meta": None,
    }


def test_health_rejects_invalid_level_with_error_envelope(client):
    response = client.get("/health", params={"level": "not-an-int"})

    assert response.status_code == 422
    body = response.json()

    assert body["success"] is False
    assert body["data"] is None
    assert body["meta"] is None

    assert body["error"]["code"] == "validation_error"

    message = body["error"]["message"]
    assert isinstance(message, str)
    assert message.strip(), "error message must not be empty"
    assert "level" in message.lower(), "message should name the offending field"
    assert "int_parsing" not in message, "message must not leak raw pydantic error type"
