"""Dataset status model (Appendix A.2.22, Dataset)."""

from __future__ import annotations

from .types import (
    ADMINISTRATOR,
    CLIENT_MEMBER,
    CLIENT_OWNER,
    FOUNDER,
    NEW_RECORD,
    SYSTEM,
    TransitionRow,
    concat,
    rows,
)

ENTITY = "dataset"

STATUSES: tuple[str, ...] = ("pending scan", "available", "rejected", "quarantined", "deleted")

# Note: the Appendix A.2.22 profiling Job statuses (queued, running, completed, failed) map to the
# Job statuses Queued, Running, Succeeded, Failed (see job.py). They are not a separate table.

# The creation row is "(complete-upload)" in Appendix A; it uses the NEW_RECORD sentinel.
TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "pending scan", (SYSTEM,),
         ("object_exists", "permission_confirmation_recorded", "guest_request_401"), 4),
    rows(ENTITY, "pending scan", "rejected", (SYSTEM,),
         ("extension_content_type_size_structure_or_row_count_check_failed", "delete_object"), 4),
    rows(ENTITY, "pending scan", "quarantined", (SYSTEM,), ("malware_detected_or_scanner_unavailable",), 4),
    rows(ENTITY, "pending scan", "available", (SYSTEM,), ("all_r56_20_checks_passed",), 4),
    rows(ENTITY, "available", "deleted", (CLIENT_OWNER, CLIENT_MEMBER, FOUNDER, ADMINISTRATOR),
         ("dataset_of_requester_organization_else_404", "no_approval_request_required"), 4),
    rows(ENTITY, "available", "deleted", (SYSTEM,), ("retention_period_expired_via_retention_job",), 4),
)
