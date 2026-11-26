"""Integration interfaces (design: Integration Interfaces; R3.3, R3.4, R3.5).

No implementation may report success when the underlying operation failed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Protocol


class IntegrationError(RuntimeError):
    """Base error for integration failures. Callers must treat it as failure."""


class StorageError(IntegrationError):
    pass


class AuthUnavailableError(IntegrationError):
    """Auth provider unavailable or disabled; no session may be created."""


class EmailSendError(IntegrationError):
    pass


class ModelInvocationError(IntegrationError):
    """Model call failed; no partial output is returned."""


class StorageClient(Protocol):
    def put(self, key: str, data: bytes) -> None: ...

    def get(self, key: str) -> bytes: ...

    def delete(self, key: str) -> None: ...


@dataclass(frozen=True)
class AuthIdentity:
    subject: str
    roles: tuple[str, ...] = ()


class AuthProvider(Protocol):
    def issue_token(self, subject: str, roles: tuple[str, ...] = ()) -> str: ...

    def verify_token(self, token: str) -> AuthIdentity:
        """Return the identity or raise AuthUnavailableError / ValueError."""
        ...


ScanStatus = Literal["clean", "infected", "unavailable"]


@dataclass(frozen=True)
class ScanResult:
    status: ScanStatus
    detail: str = ""


class MalwareScanner(Protocol):
    def scan(self, data: bytes, filename: str) -> ScanResult: ...


@dataclass(frozen=True)
class EmailMessage:
    to: str
    subject: str
    body: str
    headers: dict[str, str] = field(default_factory=dict)


class EmailSender(Protocol):
    def send(self, message: EmailMessage) -> None:
        """Raise EmailSendError on failure."""
        ...


class NotificationChannel(Protocol):
    def notify(self, user_id: str, subject: str, body: str) -> None: ...


class ModelClient(Protocol):
    def invoke(self, prompt: str, *, model: str | None = None) -> str:
        """Return the full output or raise ModelInvocationError."""
        ...
