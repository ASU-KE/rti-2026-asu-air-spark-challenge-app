from fastapi.testclient import TestClient


def test_health_reports_ok_in_the_standard_envelope(client: TestClient) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    # Exact equality also pins the contract the frontend client relies on:
    # `meta` is absent unless the payload is a paginated collection.
    assert response.json() == {
        "success": True,
        "data": {"status": "ok"},
        "error": None,
    }
