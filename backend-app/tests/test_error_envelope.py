"""Failures must reach the client in the same envelope as successes."""

from collections.abc import Iterator
from contextlib import contextmanager

import httpx
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.main import create_app


def test_unknown_route_returns_an_error_envelope(client: TestClient) -> None:
    response = client.get("/api/does-not-exist")

    assert_error_envelope(response, status_code=404, mentions="Not Found")


def test_invalid_request_body_returns_a_user_friendly_error_envelope() -> None:
    with probe_client() as client:
        response = client.post("/api/_probe", json={"rounds": "many"})

    assert_error_envelope(response, status_code=422, mentions="rounds")


def test_missing_required_field_names_the_field() -> None:
    with probe_client() as client:
        response = client.post("/api/_probe", json={})

    assert_error_envelope(response, status_code=422, mentions="rounds")


def test_unexpected_failure_returns_a_generic_error_envelope() -> None:
    leaky_message = "connect failed for key sk-provider-do-not-leak"

    # `raise_server_exceptions=False` lets the app answer rather than re-raise
    # into the test, which is how it behaves behind a real server.
    with probe_client(raise_server_exceptions=False) as client:
        response = client.get("/api/_explode", params={"reason": leaky_message})

    assert_error_envelope(response, status_code=500, mentions="Internal server error")
    assert leaky_message not in response.text


def assert_error_envelope(
    response: httpx.Response, *, status_code: int, mentions: str
) -> None:
    """Assert a failure arrived in the standard envelope, naming its cause."""
    assert response.status_code == status_code
    body = response.json()
    assert body["success"] is False
    assert body["data"] is None
    assert mentions in body["error"]
    # FastAPI's default `detail` shape would break the frontend client.
    assert "detail" not in body


class _ProbePayload(BaseModel):
    rounds: int


@contextmanager
def probe_client(*, raise_server_exceptions: bool = True) -> Iterator[TestClient]:
    """A real app plus routes that take input and that fail unexpectedly.

    No endpoint in this slice accepts input or can crash, so those boundary
    behaviours are exercised through probe routes registered on the real
    application — the same handlers and middleware run as for a real route.
    """
    app = create_app()

    @app.post("/api/_probe")
    def probe(payload: _ProbePayload) -> dict[str, int]:
        return {"rounds": payload.rounds}

    @app.get("/api/_explode")
    def explode(reason: str) -> None:
        raise RuntimeError(reason)

    with TestClient(app, raise_server_exceptions=raise_server_exceptions) as test:
        yield test
