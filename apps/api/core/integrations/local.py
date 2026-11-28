"""Local adapters. None of them returns fabricated success (R3.4)."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import secrets
from collections.abc import Mapping
from pathlib import Path

from core.integrations.interfaces import (
    AuthIdentity,
    AuthUnavailableError,
    EmailMessage,
    EmailSendError,
    ModelInvocationError,
    ScanResult,
    StorageError,
)

logger = logging.getLogger(__name__)


class FilesystemStorage:
    """Stands in for S3. Keys are confined to the root directory."""

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root).resolve()

    def _path(self, key: str) -> Path:
        path = (self._root / key).resolve()
        if path == self._root or self._root not in path.parents:
            raise StorageError(f"Invalid storage key: {key!r}")
        return path

    def put(self, key: str, data: bytes) -> None:
        path = self._path(key)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        except OSError as exc:
            raise StorageError(f"Could not write {key!r}") from exc

    def get(self, key: str) -> bytes:
        try:
            return self._path(key).read_bytes()
        except OSError as exc:
            raise StorageError(f"Could not read {key!r}") from exc

    def delete(self, key: str) -> None:
        try:
            self._path(key).unlink()
        except OSError as exc:
            raise StorageError(f"Could not delete {key!r}") from exc


class LocalDevAuthProvider:
    """Development tokens (HMAC-signed). Usable only when ENVIRONMENT=local."""

    def __init__(self, environment: str, signing_key: str | None = None) -> None:
        if environment != "local":
            raise AuthUnavailableError("Local dev auth is enabled only when ENVIRONMENT=local")
        self._key = (signing_key or secrets.token_hex(32)).encode()

    def _sign(self, payload: str) -> str:
        return hmac.new(self._key, payload.encode(), hashlib.sha256).hexdigest()

    def issue_token(self, subject: str, roles: tuple[str, ...] = ()) -> str:
        payload = base64.urlsafe_b64encode(
            json.dumps({"sub": subject, "roles": list(roles)}).encode()
        ).decode()
        return f"dev.{payload}.{self._sign(payload)}"

    def verify_token(self, token: str) -> AuthIdentity:
        parts = token.split(".")
        if len(parts) != 3 or parts[0] != "dev":
            raise ValueError("Malformed token")
        if not hmac.compare_digest(parts[2], self._sign(parts[1])):
            raise ValueError("Invalid token signature")
        data = json.loads(base64.urlsafe_b64decode(parts[1]))
        return AuthIdentity(subject=data["sub"], roles=tuple(data["roles"]))


class StubMalwareScanner:
    """Always reports 'unavailable' so files stay quarantined (R3.4, R20.9)."""

    def scan(self, data: bytes, filename: str) -> ScanResult:
        return ScanResult(status="unavailable", detail="scanner unavailable")


class OutboxEmailSender:
    """Appends messages to a JSONL outbox file and logs them. Nothing is sent."""

    def __init__(self, outbox_path: str | Path) -> None:
        self._path = Path(outbox_path)

    def send(self, message: EmailMessage) -> None:
        record = {
            "to": message.to,
            "subject": message.subject,
            "body": message.body,
            "headers": message.headers,
        }
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(record) + "\n")
        except OSError as exc:
            raise EmailSendError("Could not write to the email outbox") from exc
        logger.info("Email written to outbox: to=%s subject=%s", message.to, message.subject)


class LogNotificationChannel:
    """Logs internal notifications. Nothing is delivered (R3.4).

    Only the recipient and subject are logged; the body may carry submitted content.
    """

    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def notify(self, user_id: str, subject: str, body: str) -> None:
        self.sent.append((user_id, subject))
        logger.info("Notification recorded: to=%s subject=%s", user_id, subject)


class RecordedModelClient:
    """Returns recorded responses keyed by prompt; no Bedrock call is made.

    An unrecorded prompt fails; it never yields invented output.
    """

    def __init__(self, responses: Mapping[str, str]) -> None:
        self._responses = dict(responses)

    def invoke(self, prompt: str, *, model: str | None = None) -> str:
        try:
            return self._responses[prompt]
        except KeyError:
            raise ModelInvocationError("No recorded response for this prompt") from None
