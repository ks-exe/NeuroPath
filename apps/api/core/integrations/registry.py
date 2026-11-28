"""Registry of active local substitutions for the implementation status record (R3.4)."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Substitution:
    interface: str
    local_adapter: str
    deployed_target: str
    note: str


class SubstitutionRegistry:
    def __init__(self) -> None:
        self._items: dict[str, Substitution] = {}

    def register(
        self, interface: str, local_adapter: str, deployed_target: str, note: str = ""
    ) -> None:
        self._items[interface] = Substitution(interface, local_adapter, deployed_target, note)

    def unregister(self, interface: str) -> None:
        self._items.pop(interface, None)

    def list_active(self) -> list[Substitution]:
        return sorted(self._items.values(), key=lambda s: s.interface)

    def as_records(self) -> list[dict[str, str]]:
        return [asdict(s) for s in self.list_active()]


# Known substitutions, keyed by interface (design: Integration Interfaces).
LOCAL_SUBSTITUTIONS: dict[str, tuple[str, str, str]] = {
    "StorageClient": ("FilesystemStorage", "Private Amazon S3 buckets", ""),
    "AuthProvider": (
        "LocalDevAuthProvider",
        "Amazon Cognito",
        "Enabled only when ENVIRONMENT=local",
    ),
    "MalwareScanner": (
        "StubMalwareScanner",
        "Not yet chosen (A-16)",
        "Always reports unavailable; files stay quarantined",
    ),
    "EmailSender": (
        "OutboxEmailSender",
        "Email provider (Appendix C)",
        "Writes to outbox file/log",
    ),
    "NotificationChannel": (
        "LogNotificationChannel",
        "Internal notification channel (Appendix C)",
        "Logs recipient and subject only; nothing is delivered",
    ),
    "ModelClient": ("RecordedModelClient", "Amazon Bedrock", "Recorded responses; no Bedrock call"),
}


def register_local(registry: SubstitutionRegistry, interface: str) -> None:
    """Record that the local adapter for `interface` is active."""
    adapter, target, note = LOCAL_SUBSTITUTIONS[interface]
    registry.register(interface, adapter, target, note)
