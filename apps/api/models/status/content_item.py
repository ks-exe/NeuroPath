"""content_items status model (Appendix A.2.25).

Internal_Agents create Drafts only and hold no status transition.
"""

from __future__ import annotations

from .types import AUTHORIZED_APPROVER, DELEGATE, FOUNDER, NEW_RECORD, TransitionRow, concat, rows

ENTITY = "content_item"

STATUSES: tuple[str, ...] = ("Draft", "In Review", "Approved", "Scheduled", "Published", "Rejected")

# content_items is created in Phase 5 (Appendix B, Optional).
TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Draft", ("Content or Marketing Internal_Agent", FOUNDER),
         ("each_claim_lists_verified_record_or_flagged_unsupported",), 5),
    rows(ENTITY, "Draft", "In Review", (FOUNDER, DELEGATE), (), 5),
    rows(ENTITY, "In Review", "Approved", (AUTHORIZED_APPROVER,), ("no_claim_flagged_unsupported",), 5),
    rows(ENTITY, "In Review", "Rejected", (AUTHORIZED_APPROVER,), ("non_empty_reason",), 5),
    rows(ENTITY, "Rejected", "Draft", (FOUNDER,), (), 5),
    rows(ENTITY, "Approved", "Scheduled", (FOUNDER, DELEGATE), (), 5),
    rows(ENTITY, ("Approved", "Scheduled"), "Published", ("System (OPS)",),
         ("approved_approval_request_hash_equals_content_item_hash",), 5),
)
