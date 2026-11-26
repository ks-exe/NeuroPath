"""Maintenance_Engagement status model (Appendix A.2.18)."""

from __future__ import annotations

from .types import ADMINISTRATOR, FOUNDER, NEW_RECORD, PROJECT_MANAGER, TransitionRow, concat, rows

ENTITY = "maintenance_engagement"

STATUSES: tuple[str, ...] = ("Proposed", "Active", "Suspended", "Ended")

_ROLES = (FOUNDER, ADMINISTRATOR, PROJECT_MANAGER)

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Proposed", _ROLES,
         ("exactly_one_originating_project_same_organization", "scope_description_present"), 4),
    rows(ENTITY, "Proposed", "Active", _ROLES, ("agreement_in_effect", "audit_log_on_guard_failure"), 4),
    rows(ENTITY, "Active", "Suspended", _ROLES, ("non_empty_reason",), 4),
    rows(ENTITY, "Suspended", "Active", _ROLES, ("agreement_in_effect",), 4),
    rows(ENTITY, ("Active", "Suspended"), "Ended", _ROLES, ("non_empty_reason",), 4),
    rows(ENTITY, "Proposed", "Ended", _ROLES, ("non_empty_reason",), 4),
)
