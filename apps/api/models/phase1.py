"""Phase 1 tables (Appendix B.3 Phase 1; R6.1, R6.3-R6.5, R14.10, R24.1).

Only the Phase 1 columns are defined here. Later phases add their columns
through their own migrations (for example `leads.status`, `projects.prior_status`).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    Uuid,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, CreatedAtMixin, IdMixin, TenantOwned, TimestampMixin
from .status import project as project_status

# Fixed id of the NEUROPATH internal Organization seeded by migration 0002 (B.1 item 5).
INTERNAL_ORGANIZATION_ID = uuid.UUID("00000000-0000-4000-8000-000000000001")
INTERNAL_ORGANIZATION_NAME = "NEUROPATH"

ORGANIZATION_KINDS: tuple[str, ...] = ("internal", "client")
CONSENT_TYPES: tuple[str, ...] = ("contact_and_processing", "ai_processing", "model_training")
ENTRY_PATHS: tuple[str, ...] = (
    "inquiry_form",
    "engineering_service_request",
    "solution_architect_lab",
)
ACTOR_TYPES: tuple[str, ...] = ("user", "agent", "system")

JSON_TYPE = JSON().with_variant(JSONB(), "postgresql")


def in_check(column: str, values: tuple[str, ...]) -> str:
    """SQL text for `column IN (...)`; values are code constants without quotes."""
    return f"{column} IN ({', '.join(repr(v) for v in values)})"


class Organization(IdMixin, TimestampMixin, Base):
    __tablename__ = "organizations"
    __table_args__ = (
        CheckConstraint(in_check("kind", ORGANIZATION_KINDS), name="kind_valid"),
        # At most one internal Organization (B.3: partial unique on kind).
        Index(
            "uq_organizations_kind_internal",
            "kind",
            unique=True,
            postgresql_where=text("kind = 'internal'"),
            sqlite_where=text("kind = 'internal'"),
        ),
    )

    name: Mapped[str] = mapped_column(Text, nullable=False)
    kind: Mapped[str] = mapped_column(String(20), nullable=False)


class Lead(IdMixin, TimestampMixin, Base):
    """Internal table (owner I): no organization_id."""

    __tablename__ = "leads"

    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    company: Mapped[str | None] = mapped_column(Text, nullable=True)
    # SHA-256 hex of the normalized email (R22.4). Not unique: duplicates are flagged (R22.5).
    email_normalized_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)


class ProjectInquiry(IdMixin, TimestampMixin, TenantOwned, Base):
    __tablename__ = "project_inquiries"
    __table_args__ = (
        CheckConstraint(in_check("entry_path", ENTRY_PATHS), name="entry_path_valid"),
        Index("ix_project_inquiries_organization_id_created_at", "organization_id", "created_at"),
    )

    lead_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("leads.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    # Client-generated idempotency token (R14.14).
    submission_token: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    problem_description: Mapped[str] = mapped_column(Text, nullable=False)
    desired_outcome: Mapped[str | None] = mapped_column(Text, nullable=True)
    existing_systems: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_and_integrations: Mapped[str | None] = mapped_column(Text, nullable=True)
    expected_users: Mapped[str | None] = mapped_column(Text, nullable=True)
    constraints: Mapped[str | None] = mapped_column(Text, nullable=True)
    budget_range: Mapped[str | None] = mapped_column(Text, nullable=True)
    preferred_timeline: Mapped[str | None] = mapped_column(Text, nullable=True)
    service_hint: Mapped[str | None] = mapped_column(Text, nullable=True)
    entry_path: Mapped[str] = mapped_column(String(40), nullable=False)


class Project(IdMixin, TimestampMixin, TenantOwned, Base):
    __tablename__ = "projects"
    __table_args__ = (
        # Generated from the Appendix A.1 status set so DB and engine agree.
        CheckConstraint(in_check("status", project_status.STATUSES), name="status_valid"),
        Index("ix_projects_organization_id_status", "organization_id", "status"),
        Index("ix_projects_organization_id_created_at", "organization_id", "created_at"),
    )

    # One Project per Project_Inquiry (R24.15, A-01).
    project_inquiry_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("project_inquiries.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    # Set only through the transition engine (T01 creates Submitted); no default.
    status: Mapped[str] = mapped_column(String(40), nullable=False)


class ConsentRecord(IdMixin, CreatedAtMixin, Base):
    """Append-only (a change is a new row). Internal, with nullable organization_id."""

    __tablename__ = "consent_records"
    __table_args__ = (
        CheckConstraint(in_check("consent_type", CONSENT_TYPES), name="consent_type_valid"),
        Index("ix_consent_records_organization_id_consent_type", "organization_id", "consent_type"),
    )

    lead_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("leads.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("organizations.id", ondelete="RESTRICT"), nullable=True
    )
    project_inquiry_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("project_inquiries.id", ondelete="RESTRICT"), nullable=True
    )
    # ai_processing is the AI-processing flag (R14.10) as its own consent row.
    consent_type: Mapped[str] = mapped_column(String(40), nullable=False)
    granted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    wording_version: Mapped[str] = mapped_column(String(64), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class AuditLog(IdMixin, CreatedAtMixin, Base):
    """Append-only (trigger in a later migration). Full R30.1 column set."""

    __tablename__ = "audit_logs"
    __table_args__ = (
        CheckConstraint(in_check("actor_type", ACTOR_TYPES), name="actor_type_valid"),
        Index("ix_audit_logs_organization_id_created_at", "organization_id", "created_at"),
    )

    actor_type: Mapped[str] = mapped_column(String(20), nullable=False)
    # FK to users is added in Phase 2 when `users` exists.
    actor_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    # Nullable for Guest and system events.
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("organizations.id", ondelete="RESTRICT"), nullable=True
    )
    request_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Redacted per R30.3. `metadata` is reserved on declarative classes.
    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSON_TYPE, nullable=False, default=dict
    )
