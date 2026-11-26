"""Project_Requirements_Version status model (Appendix A.2.7).

No requirement defines a transition out of Draft. A Confirmed status is a
proposal pending Founder review and is not encoded.
"""

from __future__ import annotations

from .types import NEW_RECORD, SYSTEM, TransitionRow, concat, rows

ENTITY = "project_requirements_version"

STATUSES: tuple[str, ...] = ("Draft",)

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "Draft", (SYSTEM,),
         ("output_passed_schema_validation", "requested_by_authorized_reviewer_or_engineer"), 3),
)
