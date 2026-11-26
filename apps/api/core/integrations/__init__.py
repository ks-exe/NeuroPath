"""Integration interfaces, local adapters and the substitution registry."""

from core.integrations.interfaces import (
    AuthIdentity,
    AuthProvider,
    AuthUnavailableError,
    EmailMessage,
    EmailSender,
    EmailSendError,
    IntegrationError,
    MalwareScanner,
    ModelClient,
    ModelInvocationError,
    NotificationChannel,
    ScanResult,
    StorageClient,
    StorageError,
)
from core.integrations.local import (
    FilesystemStorage,
    LocalDevAuthProvider,
    OutboxEmailSender,
    RecordedModelClient,
    StubMalwareScanner,
)
from core.integrations.registry import (
    LOCAL_SUBSTITUTIONS,
    Substitution,
    SubstitutionRegistry,
    register_local,
)

__all__ = [
    "AuthIdentity",
    "AuthProvider",
    "AuthUnavailableError",
    "EmailMessage",
    "EmailSendError",
    "EmailSender",
    "FilesystemStorage",
    "IntegrationError",
    "LOCAL_SUBSTITUTIONS",
    "LocalDevAuthProvider",
    "MalwareScanner",
    "ModelClient",
    "ModelInvocationError",
    "NotificationChannel",
    "OutboxEmailSender",
    "RecordedModelClient",
    "ScanResult",
    "StorageClient",
    "StorageError",
    "StubMalwareScanner",
    "Substitution",
    "SubstitutionRegistry",
    "register_local",
]
