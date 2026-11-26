"""Project_Milestone status model (Appendix A.2.11)."""

from __future__ import annotations

from .types import (
    CLIENT_MEMBER,
    CLIENT_OWNER,
    FOUNDER,
    NEW_RECORD,
    PROJECT_MANAGER,
    STAFF_ASSIGNED,
    TransitionRow,
    concat,
    rows,
)

ENTITY = "project_milestone"

STATUSES: tuple[str, ...] = ("Planned", "In Progress", "Ready for Review", "Accepted", "Rejected")
TERMINAL_STATUSES: frozenset[str] = frozenset({"Accepted"})

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Planned", (STAFF_ASSIGNED,), ("name_and_dates_present_due_not_before_start",), 4),
    rows(ENTITY, "Planned", "In Progress", (STAFF_ASSIGNED,), (), 4),
    rows(ENTITY, "In Progress", "Ready for Review", (STAFF_ASSIGNED,), (), 4),
    rows(ENTITY, "Ready for Review", "Accepted", (CLIENT_OWNER, CLIENT_MEMBER, FOUNDER),
         ("client_member_has_decision_permission", "founder_off_platform_with_evidence",
          "milestone_client_visible", "create_acceptance_record"), 4),
    rows(ENTITY, "Ready for Review", "Rejected", (CLIENT_OWNER, CLIENT_MEMBER),
         ("client_member_has_decision_permission", "milestone_client_visible",
          "non_empty_reason_in_acceptance_record"), 4),
    rows(ENTITY, "Rejected", "In Progress", (STAFF_ASSIGNED,), (), 4),
    rows(ENTITY, "Ready for Review", "Accepted", (PROJECT_MANAGER, FOUNDER),
         ("project_manager_is_current_project_member", "milestone_internal_only"), 4),
)
