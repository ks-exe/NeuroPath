"""Empty baseline (Appendix B.3, Phase 0: no tables).

Revision ID: 0001_baseline
Revises:
Create Date: 2025-01-01 00:00:00
"""

from collections.abc import Sequence

revision: str = "0001_baseline"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
