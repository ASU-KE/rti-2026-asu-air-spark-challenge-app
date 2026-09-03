"""Application entrypoint and factory for the ASU AIR Spark Challenge backend.

``create_app`` is the single place where middleware, exception handlers, and
routers are registered, so later slices can extend the app without touching
route code. A module-level ``app`` instance is exposed for
``uvicorn app.main:app``.
"""
from fastapi import FastAPI

from app.envelope import success

__all__ = ["app", "create_app"]


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    application = FastAPI(title="ASU AIR Spark Challenge Backend")

    @application.get("/health")
    def read_health() -> dict:
        """Liveness probe returning the standard success envelope."""
        return success({"status": "ok"})

    return application


app = create_app()
