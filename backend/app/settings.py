"""Server-side configuration loaded from the environment.

Settings are server-side only and are never serialized into a response. The
provider API key is read from the ``PROVIDER_API_KEY`` environment variable
and is optional (``None`` when unset). ``get_settings`` is the dependency
future slices use to access configuration without leaking it to clients.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings

__all__ = ["Settings", "get_settings"]


class Settings(BaseSettings):
    """Application settings sourced from environment variables.

    Field names map to same-named (uppercased) env vars with no prefix, so
    ``provider_api_key`` reads ``PROVIDER_API_KEY``.
    """

    provider_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance for use as a FastAPI dependency."""
    return Settings()
