"""Job status model (Appendix A.2.23)."""

from __future__ import annotations

from .types import (
    ADMINISTRATOR,
    FOUNDER,
    INTERNAL_AGENT,
    JOB_OWNER,
    NEW_RECORD,
    SYSTEM,
    TransitionRow,
    concat,
    rows,
)

ENTITY = "job"

STATUSES: tuple[str, ...] = ("Queued", "Running", "Succeeded", "Failed", "Cancelled")

# Jobs table is created in Phase 2 (Appendix B).
TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Queued", (SYSTEM, FOUNDER, ADMINISTRATOR, INTERNAL_AGENT + " (requester only)"),
         ("job_type_in_registry_else_reject_and_audit", "parameters_pass_job_type_schema",
          "dedupe_key_present_matching_key_returns_existing_job"), 2),
    rows(ENTITY, "Queued", "Running", ("System worker",), (), 2),
    rows(ENTITY, "Running", "Succeeded", (SYSTEM,), ("registered_handler_completed",), 2),
    rows(ENTITY, "Running", "Failed", (SYSTEM,),
         ("retries_exhausted_or_limit_exceeded_or_out_of_permission_request",
          "dead_letter_record_and_notification"), 2),
    rows(ENTITY, "Running", "Queued", (SYSTEM,), ("transient_failure_with_fewer_than_3_retries",), 2),
    rows(ENTITY, ("Queued", "Running"), "Cancelled", (JOB_OWNER, FOUNDER, ADMINISTRATOR), (), 2),
)
