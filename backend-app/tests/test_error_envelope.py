"""Failures must reach the client in the same envelope as successes."""

from collections.abc import Iterator
from contextlib import contextmanager

from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.main import create_app


def test_unknown_route_returns_an_error_envelope(client: TestClient) -> None:
    response = client.get("/api/does-not-exist")

    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"] == "Not Found"
    # FastAPI's default `detail` shape would break the frontend client.
    assert "detail" not in body


def test_invalid_request_body_returns_a_user_friendly_error_envelope() -> None:
    with _probe_client() as client:
        response = client.post("/api/_probe", json={"rounds": "many"})

    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["data"] is None
    assert "rounds" in body["error"]
    assert "detail" not in body


def test_missing_required_field_names_the_field() -> None:
    with _probe_client() as client:
        response = client.post("/api/_probe", json={})

    assert response.status_code == 422
    assert "rounds" in response.json()["error"]


class _ProbePayload(BaseModel):
    rounds: int


@contextmanager
def _probe_client() -> Iterator[TestClient]:
    """A real app plus one route that accepts a schema-validated body.

    No endpoint in this slice takes input, so boundary validation is exercised
    through a probe route registered on the real application — the same
    exception handlers and middleware run as for a production route.
    """
    app = create_app()

    @app.post("/api/_probe")
    def probe(payload: _ProbePayload) -> dict[str, int]:
        return {"rounds": payload.rounds}

    with TestClient(app) as test_client:
        yield test_client



def test_unexpected_failure_returns_a_generic_error_envelope() -> None:
    app = create_app()
    leaky_message = "connect failed for key sk-provider-do-not-leak"

    @app.get("/api/_explode")
    def explode() -> None:
        raise RuntimeError(leaky_message)

    # Let the app answer instead of re-raising, as it would in production.
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/api/_explode")

    assert response.status_code == 500
    assert response.json() == {
        "success": False,
        "data": None,
        "error": "Internal server error",
    }
    assert leaky_message not in response.text
