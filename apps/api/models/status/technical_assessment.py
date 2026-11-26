"""Technical_Assessment_Version status model (Appendix A.2.5)."""

from __future__ import annotations

from .types import ASSIGNED_ENGINEER, FOUNDER, NEW_RECORD, TransitionRow, concat, rows

ENTITY = "technical_assessment_version"

STATUSES: tuple[str, ...] = ("Unconfirmed", "Confirmed")

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Unconfirmed", ("Agent_Runtime Job requested by Assigned Engineer or Founder",),
         ("stored_analysis_exists", "labels_from_six_service_groups", "complexity_has_justification"), 3),
    rows(ENTITY, NEW_RECORD, "Confirmed", (ASSIGNED_ENGINEER, FOUNDER),
         ("manual_or_edited_version_validation_passes",), 2),
    rows(ENTITY, "Unconfirmed", "Confirmed", (ASSIGNED_ENGINEER, FOUNDER),
         ("record_confirming_user_and_timestamp", "other_roles_receive_403"), 2),
)
