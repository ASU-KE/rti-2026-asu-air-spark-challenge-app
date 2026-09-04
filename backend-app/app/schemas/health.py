"""Schema for the health check payload."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthStatus(BaseModel):
    """Liveness report carried in the envelope's ``data`` field."""

    model_config = ConfigDict(frozen=True)

    status: Literal["ok"]
