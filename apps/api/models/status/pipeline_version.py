"""Pipeline version approval status model (Appendix A.2.22, Pipeline version approval)."""

from __future__ import annotations

from .types import (
    ADMINISTRATOR,
    CLIENT_MEMBER,
    CLIENT_OWNER,
    ENGINEER,
    FOUNDER,
    PROJECT_MANAGER,
    SYSTEM,
    TransitionRow,
    concat,
    rows,
)

ENTITY = "pipeline_version"

STATUSES: tuple[str, ...] = ("unapproved", "approved")

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, "unapproved", "approved",
         (CLIENT_OWNER, CLIENT_MEMBER, FOUNDER, ADMINISTRATOR, ENGINEER, PROJECT_MANAGER),
         ("validation_passes", "destructive_operations_confirmed_by_name"), 4),
    rows(ENTITY, "approved", "unapproved", (SYSTEM,),
         ("pipeline_changed_after_approval_creates_new_version_and_clears_approval",), 4),
)
