"""Handover_Checklist item status model (Appendix A.2.16)."""

from __future__ import annotations

from .types import FOUNDER, NEW_RECORD, PROJECT_MANAGER, STAFF_ASSIGNED, TransitionRow, concat, rows

ENTITY = "handover_checklist_item"

STATUSES: tuple[str, ...] = ("Open", "Done")

_ROLES = (STAFF_ASSIGNED, PROJECT_MANAGER, FOUNDER)

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Open", _ROLES, ("no_secret_pattern_match",), 4),
    rows(ENTITY, "Open", "Done", _ROLES, ("mandatory_item_has_evidence_attachment_or_note",), 4),
    rows(ENTITY, "Done", "Open", _ROLES, (), 4),
)
