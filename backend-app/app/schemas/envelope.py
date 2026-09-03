"""The standard response envelope shared by every endpoint.

The wire shape mirrors ``frontend-app/src/api/envelope.ts``:

- ``success`` — whether the request succeeded.
- ``data`` — the payload, ``null`` on error.
- ``error`` — a user-friendly message, ``null`` on success.

The frontend contract also allows an optional ``meta`` object carrying
pagination metadata. No endpoint returns a collection yet, so that variant is
deliberately absent: the first collection endpoint adds a ``PaginatedEnvelope``
subclass with a ``meta`` field, driven by its own test. Emitting ``meta: null``
on every response instead would put a field on the wire that the frontend type
declares optional.

Build responses with the helpers in this module rather than assembling the
envelope by hand, so the fields stay consistent across endpoints.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

PayloadT = TypeVar("PayloadT")


class Envelope(BaseModel, Generic[PayloadT]):
    """Envelope wrapping every API response."""

    model_config = ConfigDict(frozen=True)

    success: bool
    data: PayloadT | None
    error: str | None


def ok(data: PayloadT) -> Envelope[PayloadT]:
    """Wrap a successful payload."""
    return Envelope(success=True, data=data, error=None)
