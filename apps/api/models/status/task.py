"""Task status model (Appendix A.2.12)."""

from __future__ import annotations

from .types import NEW_RECORD, STAFF_ASSIGNED, TransitionRow, concat, rows

ENTITY = "task"

STATUSES: tuple[str, ...] = ("To Do", "In Progress", "Blocked", "Done", "Cancelled")

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "To Do", (STAFF_ASSIGNED,), ("assignee_is_current_project_member",), 4),
    rows(ENTITY, "To Do", "In Progress", (STAFF_ASSIGNED,), (), 4),
    rows(ENTITY, ("To Do", "In Progress"), "Blocked", (STAFF_ASSIGNED,), ("non_empty_reason",), 4),
    rows(ENTITY, "Blocked", "In Progress", (STAFF_ASSIGNED,), (), 4),
    rows(ENTITY, "In Progress", "Done", (STAFF_ASSIGNED,), (), 4),
    rows(ENTITY, ("To Do", "In Progress", "Blocked"), "Cancelled", (STAFF_ASSIGNED,), (), 4),
    rows(ENTITY, "Done", "In Progress", (STAFF_ASSIGNED,), (), 4),
)
