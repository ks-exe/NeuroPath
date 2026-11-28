"""Phase 1 tables and the NEUROPATH internal Organization seed (Appendix B.3 Phase 1).

Creates organizations, leads, project_inquiries, projects, consent_records and
audit_logs. The audit_logs append-only trigger is added by a later revision.

Revision ID: 0002_phase1
Revises: 0001_baseline
Create Date: 2025-01-02 00:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op
from models.phase1 import (
    ACTOR_TYPES,
    CONSENT_TYPES,
    ENTRY_PATHS,
    INTERNAL_ORGANIZATION_ID,
    INTERNAL_ORGANIZATION_NAME,
    ORGANIZATION_KINDS,
    in_check,
)
from models.status.project import STATUSES as PROJECT_STATUSES

revision: str = "0002_phase1"
down_revision: str | None = "0001_baseline"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_JSON = sa.JSON().with_variant(postgresql.JSONB(), "postgresql")


def _id() -> sa.Column:
    return sa.Column("id", sa.Uuid(), nullable=False)


def _created_at() -> sa.Column:
    return sa.Column(
        "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )


def _updated_at() -> sa.Column:
    return sa.Column(
        "updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )


def _org_fk(table: str) -> sa.ForeignKeyConstraint:
    return sa.ForeignKeyConstraint(
        ["organization_id"],
        ["organizations.id"],
        name=f"fk_{table}_organization_id_organizations",
        ondelete="RESTRICT",
    )


def upgrade() -> None:
    op.create_table(
        "organizations",
        _id(),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("kind", sa.String(length=20), nullable=False),
        _created_at(),
        _updated_at(),
        sa.CheckConstraint(
            in_check("kind", ORGANIZATION_KINDS), name="ck_organizations_kind_valid"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_organizations"),
    )
    op.create_index(
        "uq_organizations_kind_internal",
        "organizations",
        ["kind"],
        unique=True,
        postgresql_where=sa.text("kind = 'internal'"),
        sqlite_where=sa.text("kind = 'internal'"),
    )

    op.create_table(
        "leads",
        _id(),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("company", sa.Text(), nullable=True),
        sa.Column("email_normalized_hash", sa.String(length=64), nullable=False),
        _created_at(),
        _updated_at(),
        sa.PrimaryKeyConstraint("id", name="pk_leads"),
    )
    op.create_index("ix_leads_email_normalized_hash", "leads", ["email_normalized_hash"])

    op.create_table(
        "project_inquiries",
        _id(),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("lead_id", sa.Uuid(), nullable=False),
        sa.Column("submission_token", sa.String(length=64), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("problem_description", sa.Text(), nullable=False),
        sa.Column("desired_outcome", sa.Text(), nullable=True),
        sa.Column("existing_systems", sa.Text(), nullable=True),
        sa.Column("data_and_integrations", sa.Text(), nullable=True),
        sa.Column("expected_users", sa.Text(), nullable=True),
        sa.Column("constraints", sa.Text(), nullable=True),
        sa.Column("budget_range", sa.Text(), nullable=True),
        sa.Column("preferred_timeline", sa.Text(), nullable=True),
        sa.Column("service_hint", sa.Text(), nullable=True),
        sa.Column("entry_path", sa.String(length=40), nullable=False),
        _created_at(),
        _updated_at(),
        sa.CheckConstraint(
            in_check("entry_path", ENTRY_PATHS), name="ck_project_inquiries_entry_path_valid"
        ),
        _org_fk("project_inquiries"),
        sa.ForeignKeyConstraint(
            ["lead_id"],
            ["leads.id"],
            name="fk_project_inquiries_lead_id_leads",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_project_inquiries"),
        sa.UniqueConstraint("submission_token", name="uq_project_inquiries_submission_token"),
    )
    op.create_index(
        "ix_project_inquiries_organization_id", "project_inquiries", ["organization_id"]
    )
    op.create_index(
        "ix_project_inquiries_organization_id_created_at",
        "project_inquiries",
        ["organization_id", "created_at"],
    )
    op.create_index("ix_project_inquiries_lead_id", "project_inquiries", ["lead_id"])

    op.create_table(
        "projects",
        _id(),
        sa.Column("organization_id", sa.Uuid(), nullable=False),
        sa.Column("project_inquiry_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        _created_at(),
        _updated_at(),
        sa.CheckConstraint(in_check("status", PROJECT_STATUSES), name="ck_projects_status_valid"),
        _org_fk("projects"),
        sa.ForeignKeyConstraint(
            ["project_inquiry_id"],
            ["project_inquiries.id"],
            name="fk_projects_project_inquiry_id_project_inquiries",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_projects"),
        sa.UniqueConstraint("project_inquiry_id", name="uq_projects_project_inquiry_id"),
    )
    op.create_index("ix_projects_organization_id", "projects", ["organization_id"])
    op.create_index("ix_projects_organization_id_status", "projects", ["organization_id", "status"])
    op.create_index(
        "ix_projects_organization_id_created_at", "projects", ["organization_id", "created_at"]
    )

    op.create_table(
        "consent_records",
        _id(),
        sa.Column("lead_id", sa.Uuid(), nullable=True),
        sa.Column("organization_id", sa.Uuid(), nullable=True),
        sa.Column("project_inquiry_id", sa.Uuid(), nullable=True),
        sa.Column("consent_type", sa.String(length=40), nullable=False),
        sa.Column("granted", sa.Boolean(), nullable=False),
        sa.Column("wording_version", sa.String(length=64), nullable=False),
        sa.Column(
            "recorded_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        _created_at(),
        sa.CheckConstraint(
            in_check("consent_type", CONSENT_TYPES), name="ck_consent_records_consent_type_valid"
        ),
        sa.ForeignKeyConstraint(
            ["lead_id"], ["leads.id"], name="fk_consent_records_lead_id_leads", ondelete="RESTRICT"
        ),
        _org_fk("consent_records"),
        sa.ForeignKeyConstraint(
            ["project_inquiry_id"],
            ["project_inquiries.id"],
            name="fk_consent_records_project_inquiry_id_project_inquiries",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_consent_records"),
    )
    op.create_index("ix_consent_records_lead_id", "consent_records", ["lead_id"])
    op.create_index(
        "ix_consent_records_organization_id_consent_type",
        "consent_records",
        ["organization_id", "consent_type"],
    )

    op.create_table(
        "audit_logs",
        _id(),
        sa.Column("actor_type", sa.String(length=20), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("resource_type", sa.String(length=100), nullable=False),
        sa.Column("resource_id", sa.Uuid(), nullable=True),
        sa.Column("organization_id", sa.Uuid(), nullable=True),
        sa.Column("request_id", sa.String(length=100), nullable=True),
        sa.Column("metadata", _JSON, nullable=False),
        _created_at(),
        sa.CheckConstraint(
            in_check("actor_type", ACTOR_TYPES), name="ck_audit_logs_actor_type_valid"
        ),
        _org_fk("audit_logs"),
        sa.PrimaryKeyConstraint("id", name="pk_audit_logs"),
    )
    op.create_index(
        "ix_audit_logs_organization_id_created_at", "audit_logs", ["organization_id", "created_at"]
    )

    # Seed the NEUROPATH internal Organization (Appendix B.1 item 5).
    organizations = sa.table(
        "organizations",
        sa.column("id", sa.Uuid()),
        sa.column("name", sa.Text()),
        sa.column("kind", sa.String()),
    )
    op.bulk_insert(
        organizations,
        [{"id": INTERNAL_ORGANIZATION_ID, "name": INTERNAL_ORGANIZATION_NAME, "kind": "internal"}],
    )


def downgrade() -> None:
    op.drop_index("ix_audit_logs_organization_id_created_at", table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index("ix_consent_records_organization_id_consent_type", table_name="consent_records")
    op.drop_index("ix_consent_records_lead_id", table_name="consent_records")
    op.drop_table("consent_records")
    op.drop_index("ix_projects_organization_id_created_at", table_name="projects")
    op.drop_index("ix_projects_organization_id_status", table_name="projects")
    op.drop_index("ix_projects_organization_id", table_name="projects")
    op.drop_table("projects")
    op.drop_index("ix_project_inquiries_lead_id", table_name="project_inquiries")
    op.drop_index("ix_project_inquiries_organization_id_created_at", table_name="project_inquiries")
    op.drop_index("ix_project_inquiries_organization_id", table_name="project_inquiries")
    op.drop_table("project_inquiries")
    op.drop_index("ix_leads_email_normalized_hash", table_name="leads")
    op.drop_table("leads")
    op.drop_index("uq_organizations_kind_internal", table_name="organizations")
    op.drop_table("organizations")
