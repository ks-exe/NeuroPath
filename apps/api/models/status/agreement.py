"""Agreement status model (Appendix A.2.10)."""

from __future__ import annotations

from .types import ADMINISTRATOR, FOUNDER, NEW_RECORD, SYSTEM, TransitionRow, concat, rows

ENTITY = "agreement"

STATUSES: tuple[str, ...] = ("Draft", "Pending Signature", "In Effect", "Expired", "Terminated")
TERMINAL_STATUSES: frozenset[str] = frozenset({"Expired", "Terminated"})

_STAFF = (FOUNDER, ADMINISTRATOR)

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Draft", _STAFF,
         ("acceptance_record_exists_on_proposal_version_else_422", "end_date_not_before_effective_date"), 3),
    rows(ENTITY, "Draft", "Pending Signature", _STAFF, (), 3),
    rows(ENTITY, "Pending Signature", "In Effect", _STAFF, ("signed_document_stored_as_available_attachment",), 3),
    rows(ENTITY, "In Effect", "Expired", (SYSTEM,), ("end_date_has_passed",), 3),
    rows(ENTITY, "In Effect", "Terminated", _STAFF, ("non_empty_reason",), 3),
    rows(ENTITY, ("Draft", "Pending Signature"), "Terminated", _STAFF, ("non_empty_reason",), 3),
)
