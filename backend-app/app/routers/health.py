"""Health check route."""

from fastapi import APIRouter

from app.schemas.envelope import Envelope, ok
from app.schemas.health import HealthStatus

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=Envelope[HealthStatus],
    summary="Report that the API is up",
)
def read_health() -> Envelope[HealthStatus]:
    return ok(HealthStatus(status="ok"))
