"""The provider API key is server-side configuration and must stay there.

The prototype runs locally with no authentication (ADR-0004, spec "Security"),
so the one credential in play is the LLM gateway key. It is loaded from the
environment and must never cross the HTTP boundary.
"""

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app

SENTINEL_KEY = "sk-air-sentinel-must-not-leak"


@pytest.fixture(autouse=True)
def configured_provider_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PROVIDER_API_KEY", SENTINEL_KEY)


def test_provider_api_key_is_loaded_from_the_environment() -> None:
    key = Settings().provider_api_key

    assert key is not None
    assert key.get_secret_value() == SENTINEL_KEY


def test_rendering_the_settings_does_not_expose_the_provider_api_key() -> None:
    settings = Settings()

    assert SENTINEL_KEY not in repr(settings)
    assert SENTINEL_KEY not in settings.model_dump_json()


@pytest.mark.parametrize(
    "path", ["/api/health", "/api/does-not-exist", "/openapi.json"]
)
def test_no_response_carries_the_provider_api_key(path: str) -> None:
    with TestClient(create_app()) as client:
        assert SENTINEL_KEY not in client.get(path).text
