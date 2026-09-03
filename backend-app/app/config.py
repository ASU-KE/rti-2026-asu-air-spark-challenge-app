"""Server-side configuration, loaded from the environment.

Settings are read from process environment variables, falling back to a `.env`
file in the repository root. The path is resolved from this module so the app
behaves the same whichever directory it is launched from.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=_REPOSITORY_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    app_name: str = "AIRgents of Change API"
    app_version: str = "0.1.0"
