"""Tests for server-side-only provider API key configuration (app.settings)."""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.settings import Settings


@pytest.fixture()
def client():
    return TestClient(app)


def test_provider_api_key_read_from_env(monkeypatch):
    monkeypatch.setenv("PROVIDER_API_KEY", "sentinel-key-value")

    settings = Settings()

    assert settings.provider_api_key == "sentinel-key-value"


def test_provider_api_key_none_when_unset(monkeypatch):
    monkeypatch.delenv("PROVIDER_API_KEY", raising=False)

    settings = Settings()

    assert settings.provider_api_key is None


def test_health_does_not_disclose_provider_api_key(monkeypatch, client):
    sentinel = "SECRET-SENTINEL-DO-NOT-LEAK"
    monkeypatch.setenv("PROVIDER_API_KEY", sentinel)

    response = client.get("/health")

    assert response.status_code == 200
    assert sentinel not in response.text
