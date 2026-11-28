"""Audit_Log repository: insert and read only (R6.9, R30.4).

There is deliberately no update or delete method. PostgreSQL also rejects UPDATE and
DELETE on ``audit_logs`` with a trigger (revision 0003_audit_append_only).
"""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.phase1 import AuditLog

MAX_LIST_LIMIT = 500


class AuditLogRepository:
    def insert(
        self,
        session: Session,
        *,
        actor_type: str,
        actor_id: uuid.UUID | None,
        action: str,
        resource_type: str,
        resource_id: uuid.UUID | None,
        organization_id: uuid.UUID | None,
        request_id: str | None,
        metadata: dict[str, Any],
    ) -> AuditLog:
        row = AuditLog(
            actor_type=actor_type,
            actor_id=actor_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            organization_id=organization_id,
            request_id=request_id,
            metadata_=metadata,
        )
        session.add(row)
        session.flush()
        return row

    def get(self, session: Session, audit_id: uuid.UUID) -> AuditLog | None:
        return session.get(AuditLog, audit_id)

    def list_for_organization(
        self, session: Session, organization_id: uuid.UUID, *, limit: int = 100
    ) -> list[AuditLog]:
        stmt = (
            select(AuditLog)
            .where(AuditLog.organization_id == organization_id)
            .order_by(AuditLog.created_at.desc(), AuditLog.id)
            .limit(_clamp(limit))
        )
        return list(session.scalars(stmt))

    def list_for_resource(
        self, session: Session, resource_type: str, resource_id: uuid.UUID, *, limit: int = 100
    ) -> list[AuditLog]:
        stmt = (
            select(AuditLog)
            .where(AuditLog.resource_type == resource_type, AuditLog.resource_id == resource_id)
            .order_by(AuditLog.created_at.desc(), AuditLog.id)
            .limit(_clamp(limit))
        )
        return list(session.scalars(stmt))


def _clamp(limit: int) -> int:
    return max(1, min(limit, MAX_LIST_LIMIT))
