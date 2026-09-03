"""FastAPI application factory.

`create_app` builds a fresh application (and fresh `Settings`) on every call so
tests stay hermetic. `app` is the ASGI entry point for uvicorn.
"""

from fastapi import FastAPI

from app.config import Settings
from app.errors import register_error_handlers
from app.routers import health

API_PREFIX = "/api"


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved = settings or Settings()

    application = FastAPI(
        title=resolved.app_name,
        version=resolved.app_version,
    )
    register_error_handlers(application)
    application.include_router(health.router, prefix=API_PREFIX)

    return application


app = create_app()
