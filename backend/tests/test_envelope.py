"""Contract tests for the reusable response-envelope builders (app.envelope)."""
from app.envelope import error, success


def test_success_returns_exact_success_shape():
    payload = {"status": "ok"}
    result = success(payload)

    assert set(result.keys()) == {"success", "data", "error", "meta"}
    assert result["success"] is True
    assert result["error"] is None
    assert result["meta"] is None
    assert result["data"] == payload


def test_success_accepts_none_payload():
    result = success(None)

    assert result["success"] is True
    assert result["data"] is None
    assert result["error"] is None
    assert result["meta"] is None


def test_error_returns_exact_error_shape():
    result = error("validation_error", "level must be an integer")

    assert set(result.keys()) == {"success", "data", "error", "meta"}
    assert result["success"] is False
    assert result["data"] is None
    assert result["meta"] is None
    assert result["error"] == {
        "code": "validation_error",
        "message": "level must be an integer",
    }
    assert result["error"]["code"] == "validation_error"
    assert result["error"]["message"] == "level must be an integer"


def test_success_builder_returns_fresh_dicts():
    a = success({"k": "v"})
    b = success({"k": "v"})

    assert a is not b
    a["data"]["k"] = "MUTATED"
    assert b["data"]["k"] == "v"


def test_error_builder_returns_fresh_dicts():
    a = error("c1", "m1")
    b = error("c2", "m2")

    assert a is not b
    a["error"]["code"] = "MUTATED"
    assert b["error"]["code"] == "c2"
