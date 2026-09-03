"""Map framework exceptions onto the standard response envelope.

FastAPI's defaults answer with ``{"detail": ...}`` — or plain text for an
unhandled exception — which the frontend client cannot read. Registering these
handlers means every failure reaches the client in the same shape as a success.
"""

import logging
from typing import cast

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.types import ExceptionHandler

from app.schemas.envelope import failed

_VALIDATION_FAILED = 422
_INTERNAL_ERROR = 500

# Deliberately opaque: the cause is logged server-side, never sent to a client,
# because exception text can carry credentials or connection detail.
_INTERNAL_ERROR_MESSAGE = "Internal server error"

_logger = logging.getLogger(__name__)


def register_error_handlers(app: FastAPI) -> None:
    """Attach the envelope handlers to `app`.

    Starlette types its registry against the base `Exception`, so each handler
    is cast at registration; the exception class passed alongside it is what
    guarantees the narrower type at call time.
    """
    app.add_exception_handler(
        HTTPException, cast(ExceptionHandler, _handle_http_exception)
    )
    app.add_exception_handler(
        RequestValidationError, cast(ExceptionHandler, _handle_validation_error)
    )
    app.add_exception_handler(Exception, _handle_unexpected_error)


async def _handle_http_exception(
    request: Request, exc: HTTPException
) -> JSONResponse:
    """Answer a raised `HTTPException` with its detail as the envelope error."""
    return _envelope_response(exc.status_code, str(exc.detail))


async def _handle_validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Answer a schema validation failure by naming the offending fields."""
    return _envelope_response(_VALIDATION_FAILED, _describe_validation_failure(exc))


async def _handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    """Answer an unhandled exception generically, logging the real cause."""
    _logger.exception(
        "Unhandled error serving %s %s", request.method, request.url.path
    )
    return _envelope_response(_INTERNAL_ERROR, _INTERNAL_ERROR_MESSAGE)


def _describe_validation_failure(exc: RequestValidationError) -> str:
    problems = "; ".join(
        f"{_field_name(error['loc'])}: {error['msg']}" for error in exc.errors()
    )
    return f"Request validation failed — {problems}"


def _field_name(location: tuple[int | str, ...]) -> str:
    """Render a Pydantic error location as a field path a user can act on.

    The first element names the request part (`body`, `query`, `path`); it is
    only worth reporting when nothing more specific follows it.
    """
    within_request_part = location[1:]
    if not within_request_part:
        return str(location[0]) if location else "request"
    return ".".join(str(segment) for segment in within_request_part)


def _envelope_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=failed(message).model_dump(mode="json"),
    )
