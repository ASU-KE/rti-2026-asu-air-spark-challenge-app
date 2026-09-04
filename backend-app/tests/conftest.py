"""Shared fixtures for the backend integration suite.

Tests exercise the FastAPI HTTP boundary — the project's primary seam — so the
only fixture needed here is an HTTP client bound to a freshly built app.
"""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(create_app()) as test_client:
        yield test_client
