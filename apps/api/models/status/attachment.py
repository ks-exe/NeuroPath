"""Attachment status model (Appendix A.2.3)."""

from __future__ import annotations

from .types import ADMINISTRATOR, FOUNDER, NEW_RECORD, SYSTEM, TransitionRow, concat, rows

ENTITY = "attachment"

STATUSES: tuple[str, ...] = ("pending scan", "available", "quarantined", "rejected", "deleted")

# The creation row is "(complete-upload)" in Appendix A; it uses the NEW_RECORD sentinel.
TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "pending scan", (SYSTEM,), ("object_exists_in_storage",), 2),
    rows(ENTITY, "pending scan", "rejected", (SYSTEM,),
         ("extension_content_type_or_size_check_failed", "delete_stored_object"), 2),
    rows(ENTITY, "pending scan", "available", (SYSTEM,), ("validation_passed_and_scan_clean",), 2),
    rows(ENTITY, "pending scan", "quarantined", (SYSTEM,),
         ("malware_detected_or_scanner_unavailable", "send_internal_notification"), 2),
    rows(ENTITY, "quarantined", "pending scan", (FOUNDER, ADMINISTRATOR),
         ("quarantine_reason_scanner_unavailable",), 2),
    rows(ENTITY, ("available", "quarantined"), "deleted", (FOUNDER, "Administrator (delegated)"),
         ("approved_approval_request_hash_matches_deletion_parameters",), 2),
)
