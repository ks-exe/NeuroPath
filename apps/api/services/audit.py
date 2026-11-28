"""AuditService write path (R30.1, R30.3, R30.5, R8.4).

``record`` writes one Audit_Log row inside the caller's session and flushes it. If the
write fails it raises ``ApiError(AUDIT_WRITE_FAILED)``; the caller's ``transaction()``
then rolls back the whole state change and the error handler returns the 500 envelope.
"""

from __future__ import annotations

import logging
import re
import uuid
from collections.abc import Mapping
from typing import Any

from sqlalchemy.orm import Session

from core.errors import AUDIT_WRITE_FAILED, ApiError
from core.logging import get_request_id
from models.phase1 import ACTOR_TYPES
from repositories.audit_log import AuditLogRepository

from .transitions import AuditEntry, AuditHook

logger = logging.getLogger(__name__)

REDACTED = "[REDACTED]"
MAX_STRING_LENGTH = 500
MAX_DEPTH = 6
TRUNCATION_SUFFIX = "...[truncated]"
STATUS_TRANSITION_ACTION = "status_transition"

# Metadata keys whose values are never stored (R30.3). Matched as a substring of the
# lower-cased key with "-" and " " normalised to "_".
_SENSITIVE_KEY_RE = re.compile(
    r"password|passwd|secret|token|authorization|auth_header|cookie|api_key|apikey"
    r"|private_key|credential|session_id|card|cvv|cvc|iban|ssn|signature"
)


def _is_sensitive_key(key: str) -> bool:
    return bool(_SENSITIVE_KEY_RE.search(key.lower().replace("-", "_").replace(" ", "_")))


def redact(value: Any, _depth: int = 0) -> Any:
    """Return a JSON-safe copy of ``value`` with sensitive keys masked and long strings cut."""
    if _depth > MAX_DEPTH:
        return REDACTED
    if isinstance(value, Mapping):
        return {
            str(k): REDACTED if _is_sensitive_key(str(k)) else redact(v, _depth + 1)
            for k, v in value.items()
        }
    if isinstance(value, list | tuple | set | frozenset):
        return [redact(v, _depth + 1) for v in value]
    if value is None or isinstance(value, bool | int | float):
        return value
    text = value if isinstance(value, str) else str(value)
    if len(text) > MAX_STRING_LENGTH:
        return text[:MAX_STRING_LENGTH] + TRUNCATION_SUFFIX
    return text


class AuditService:
    def __init__(self, repository: AuditLogRepository | None = None) -> None:
        self._repo = repository or AuditLogRepository()

    def record(
        self,
        session: Session,
        *,
        actor_type: str,
        actor_id: uuid.UUID | None,
        action: str,
        resource_type: str,
        resource_id: uuid.UUID | None,
        organization_id: uuid.UUID | None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        """Write one entry in the caller's transaction; raise AUDIT_WRITE_FAILED on failure."""
        try:
            if actor_type not in ACTOR_TYPES:
                raise ValueError(f"invalid actor_type {actor_type!r}")
            self._repo.insert(
                session,
                actor_type=actor_type,
                actor_id=actor_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                organization_id=organization_id,
                request_id=get_request_id(),
                metadata=redact(dict(metadata or {})),
            )
        except Exception as exc:
            logger.error(
                "audit write failed",
                extra={"audit_action": action, "resource_type": resource_type},
                exc_info=exc,
            )
            raise ApiError(AUDIT_WRITE_FAILED, "The audit record could not be written.") from exc


def _actor_of(principal: object) -> tuple[str, uuid.UUID | None]:
    actor_id = getattr(principal, "id", None) or getattr(principal, "user_id", None)
    if not isinstance(actor_id, uuid.UUID):
        actor_id = None
    declared = getattr(principal, "actor_type", None)
    if declared in ACTOR_TYPES:
        return declared, actor_id
    if actor_id is None:
        return "system", None
    return ("user" if getattr(principal, "is_human", False) else "agent"), actor_id


def transition_audit_hook(
    session: Session,
    *,
    resource_id: uuid.UUID | None,
    organization_id: uuid.UUID | None,
    service: AuditService | None = None,
) -> AuditHook:
    """Build the ``audit_hook`` for ``transition()`` writing one ``status_transition`` row."""
    svc = service or AuditService()

    def hook(entry: AuditEntry) -> None:
        actor_type, actor_id = _actor_of(entry.principal)
        svc.record(
            session,
            actor_type=actor_type,
            actor_id=actor_id,
            action=STATUS_TRANSITION_ACTION,
            resource_type=entry.entity_type,
            resource_id=resource_id,
            organization_id=organization_id,
            metadata={
                "entity": entry.entity_type,
                "from": entry.prior_status,
                "to": entry.new_status,
                "reason": entry.reason,
            },
        )

    return hook
