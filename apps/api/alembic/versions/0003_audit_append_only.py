"""Append-only audit_logs: reject UPDATE and DELETE with a trigger (R6.9, R30.4).

PostgreSQL only. On other dialects (SQLite in tests) this revision is a no-op; there the
repository's lack of update and delete methods is the only guard.

Revision ID: 0003_audit_append_only
Revises: 0002_phase1
Create Date: 2025-01-03 00:00:00
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0003_audit_append_only"
down_revision: str | None = "0002_phase1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _is_postgres() -> bool:
    return op.get_bind().dialect.name == "postgresql"


def upgrade() -> None:
    if not _is_postgres():
        return
    op.execute(
        """
        CREATE FUNCTION audit_logs_reject_change() RETURNS trigger
        LANGUAGE plpgsql AS $$
        BEGIN
            RAISE EXCEPTION 'audit_logs is append-only: % is not allowed', TG_OP
                USING ERRCODE = 'insufficient_privilege';
        END;
        $$
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_audit_logs_append_only
        BEFORE UPDATE OR DELETE ON audit_logs
        FOR EACH ROW EXECUTE FUNCTION audit_logs_reject_change()
        """
    )


def downgrade() -> None:
    if not _is_postgres():
        return
    op.execute("DROP TRIGGER IF EXISTS trg_audit_logs_append_only ON audit_logs")
    op.execute("DROP FUNCTION IF EXISTS audit_logs_reject_change()")
