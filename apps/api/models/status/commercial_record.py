"""Commercial_Record status model (Appendix A.2.20).

No Internal_Agent or AI component holds any transition (R79.7, R68.7, R68.8).
"""

from __future__ import annotations

from .types import DELEGATE, FOUNDER, NEW_RECORD, SYSTEM, TransitionRow, concat, rows

ENTITY = "commercial_record"

STATUSES: tuple[str, ...] = ("Draft", "Issued", "Paid Recorded", "Overdue", "Void")

_ROLES = (FOUNDER, DELEGATE)

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Draft", _ROLES,
         ("type_in_r79_1_set", "non_negative_amount", "iso_4217_currency", "due_date_present",
          "links_same_project_only", "no_card_or_bank_credential_pattern"), 4),
    rows(ENTITY, "Draft", "Issued", _ROLES,
         ("approved_quotation_approval_request_hash_matches", "audit_log_on_guard_failure"), 4),
    rows(ENTITY, "Issued", "Overdue", (SYSTEM,), ("current_date_after_due_date",), 4),
    rows(ENTITY, ("Issued", "Overdue"), "Paid Recorded", _ROLES,
         ("evidence_reference_present", "recording_user_and_time_stored"), 4),
    rows(ENTITY, ("Draft", "Issued", "Overdue"), "Void", _ROLES, ("non_empty_reason",), 4),
)
