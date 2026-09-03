"""Server-side configuration, loaded from the environment.

Settings are read from process environment variables, falling back to a `.env`
file in the repository root. The path is resolved from this module so the app
behaves the same whichever directory it is launched from.
"""

from pathlib import Path

from pydantic import SecretStr
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

    # ASU Research Computing LLM gateway (ADR-0004). `SecretStr` keeps the key
    # out of reprs, logs, and serialised settings; it is never sent to a client.
    # Optional for now because no code calls the gateway yet — the slice that
    # introduces the ProviderClient makes it required at startup.
    provider_api_key: SecretStr | None = None
    provider_base_url: str = "https://openai.rc.asu.edu/v1"
