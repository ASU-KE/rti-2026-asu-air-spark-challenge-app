"""Application entrypoint and factory for the ASU AIR Spark Challenge backend.

``create_app`` is the single place where middleware, exception handlers, and
routers are registered, so later slices can extend the app without touching
route code. A module-level ``app`` instance is exposed for
``uvicorn app.main:app``.
"""
from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.envelope import error, success

__all__ = ["app", "create_app"]


async def request_validation_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Reshape boundary validation failures into the standard error envelope.

    The message is derived from the first validation error and names the
    offending field; it never leaks raw pydantic/JSON error internals.
    """
    first = exc.errors()[0] if exc.errors() else None
    if first is None:
        message = "Invalid request"
    else:
        field = ".".join(str(part) for part in first["loc"])
        message = f"{field}: {first['msg']}"
    return JSONResponse(
        status_code=422, content=error("validation_error", message)
    )


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    application = FastAPI(title="ASU AIR Spark Challenge Backend")

    application.add_exception_handler(
        RequestValidationError, request_validation_handler
    )

    @application.get("/health")
    def read_health(level: int | None = Query(default=None)) -> dict:
        """Liveness probe returning the standard success envelope.

        ``level`` is an optional typed query parameter retained only to
        exercise boundary validation; its value is intentionally unused.
        """
        return success({"status": "ok"})

    return application


app = create_app()
