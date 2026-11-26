"""Defect status model (Appendix A.2.14). Severity set: A-18."""

from __future__ import annotations

from .types import FOUNDER, NEW_RECORD, STAFF_ASSIGNED, TransitionRow, concat, rows

ENTITY = "defect"

STATUSES: tuple[str, ...] = ("Open", "In Progress", "Resolved", "Verified", "Closed", "Won't Fix")
SEVERITIES: tuple[str, ...] = ("Blocker", "Critical", "Major", "Minor")

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Open", (STAFF_ASSIGNED,), ("severity_in_a18_set",), 4),
    rows(ENTITY, "Open", "In Progress", (STAFF_ASSIGNED,), (), 4),
    rows(ENTITY, "In Progress", "Resolved", (STAFF_ASSIGNED,), ("non_empty_resolution_note",), 4),
    rows(ENTITY, "Resolved", "Verified", (STAFF_ASSIGNED,), (), 4),
    rows(ENTITY, "Resolved", "In Progress", (STAFF_ASSIGNED,), (), 4),
    rows(ENTITY, "Verified", "Closed", (STAFF_ASSIGNED,), (), 4),
    rows(ENTITY, ("Open", "In Progress"), "Won't Fix", (STAFF_ASSIGNED, FOUNDER),
         ("non_empty_resolution_note", "founder_only_for_blocker_or_critical_with_recorded_approval_else_audit"), 4),
    rows(ENTITY, ("Closed", "Won't Fix"), "Open", (STAFF_ASSIGNED,), (), 4),
)
