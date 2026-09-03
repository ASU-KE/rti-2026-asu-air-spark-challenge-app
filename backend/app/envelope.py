"""Reusable response-envelope builders.

Every API response is wrapped in one consistent envelope so clients can rely
on a single shape regardless of the endpoint or the outcome:

- success: ``{"success": true, "data": <payload>, "error": null, "meta": null}``
- error:   ``{"success": false, "data": null,
              "error": {"code": <str>, "message": <str>}, "meta": null}``

``meta`` carries pagination metadata only where applicable; it is null here.
Builders are pure: each call returns a fresh dict with no shared state.
"""
from typing import Any

__all__ = ["error", "success"]


def success(data: Any) -> dict[str, Any]:
    """Build a success envelope carrying ``data`` with error and meta null."""
    return {
        "success": True,
        "data": data,
        "error": None,
        "meta": None,
    }


def error(code: str, message: str) -> dict[str, Any]:
    """Build an error envelope carrying a string ``code`` and ``message``."""
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
        },
        "meta": None,
    }
