"""Application settings and the secrets provider (R3.1, R3.2, R3.7)."""

from __future__ import annotations

import os
from collections.abc import Mapping
from functools import lru_cache
from typing import Any, Literal, Protocol

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SecretNotFoundError(RuntimeError):
    """A required secret is unavailable. Callers must fail closed."""


class SecretsProvider(Protocol):
    """Secret retrieval interface (design: Integration Interfaces)."""

    def get_secret(self, name: str) -> str:
        """Return the secret value or raise SecretNotFoundError."""
        ...


class EnvSecretsProvider:
    """Local implementation: reads secrets from environment variables."""

    def __init__(self, environ: Mapping[str, str] | None = None) -> None:
        self._environ = environ if environ is not None else os.environ

    def get_secret(self, name: str) -> str:
        value = self._environ.get(name)
        if not value:
            raise SecretNotFoundError(f"Secret '{name}' is not set in the environment")
        return value


class AwsSecretsManagerProvider:
    """AWS Secrets Manager implementation (code only; not provisioned).

    boto3 is imported lazily on first use. No credentials are configured here;
    the default AWS credential chain applies when a client is created.
    A client may be injected (tests use a fake).
    """

    def __init__(self, region_name: str | None = None, client: Any | None = None) -> None:
        self._region_name = region_name
        self._client = client

    def _get_client(self) -> Any:
        if self._client is None:
            import boto3  # lazy import

            self._client = boto3.client("secretsmanager", region_name=self._region_name)
        return self._client

    def get_secret(self, name: str) -> str:
        try:
            response = self._get_client().get_secret_value(SecretId=name)
        except Exception as exc:  # fail closed, never return a fabricated value
            raise SecretNotFoundError(f"Secret '{name}' could not be retrieved") from exc
        value = response.get("SecretString")
        if not value:
            raise SecretNotFoundError(f"Secret '{name}' has no string value")
        return str(value)


class Settings(BaseSettings):
    """Non-secret configuration. Secrets are fetched through a SecretsProvider."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: Literal["local", "dev", "staging", "prod"] = "local"
    # Highest delivered platform phase; the transition engine enables rows with
    # enabled_phase <= platform_phase (R8.6).
    platform_phase: int = Field(default=1, ge=1, validation_alias="PLATFORM_PHASE")
    database_url: str = "postgresql+psycopg://neuropath:neuropath@localhost:5432/neuropath"
    aws_region: str | None = None
    # Name of the secret holding sensitive values in deployed environments.
    secrets_backend: Literal["env", "aws"] | None = None

    # Inquiry form limits (R14.3, R14.9). Short fields are single-line; long fields keep
    # newlines and tabs.
    inquiry_short_text_max_length: int = Field(default=200, ge=1)
    inquiry_long_text_max_length: int = Field(default=5000, ge=1)
    inquiry_problem_description_min_length: int = Field(default=20, ge=1)
    # Internal recipients notified of each new Project_Inquiry (R14.12). Phase 1 has no
    # users table, so these are notification-channel addresses, never the submitter.
    inquiry_notification_recipients: list[str] = Field(default_factory=lambda: ["founder"])
    # Anonymous submissions allowed per client IP per window (R14.7).
    inquiry_rate_limit_max: int = Field(default=5, ge=1)
    inquiry_rate_limit_window_seconds: int = Field(default=600, ge=1)


def get_secrets_provider(settings: Settings) -> SecretsProvider:
    """Env variables locally, AWS Secrets Manager in deployed environments (R3.2)."""
    backend = settings.secrets_backend or ("env" if settings.environment == "local" else "aws")
    if backend == "env":
        return EnvSecretsProvider()
    return AwsSecretsManagerProvider(region_name=settings.aws_region)


@lru_cache
def get_settings() -> Settings:
    return Settings()
