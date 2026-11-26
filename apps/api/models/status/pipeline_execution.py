"""Pipeline Execution status model (Appendix A.2.22, Execution)."""

from __future__ import annotations

from .types import NEW_RECORD, SYSTEM, TransitionRow, concat, rows

ENTITY = "pipeline_execution"

STATUSES: tuple[str, ...] = ("queued", "running", "completed", "failed")

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "queued", (SYSTEM,),
         ("requested_by_user_permitted_to_approve_pipeline", "current_pipeline_version_approved_else_409_and_no_job"), 4),
    rows(ENTITY, "queued", "running", (SYSTEM,), (), 4),
    rows(ENTITY, "running", "completed", (SYSTEM,), ("every_operation_succeeded",), 4),
    rows(ENTITY, "running", "failed", (SYSTEM,),
         ("operation_failed_or_limit_exceeded_or_retries_exhausted", "send_notification"), 4),
)
