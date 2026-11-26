"""Solution_Architecture_Version status model (Appendix A.2.6)."""

from __future__ import annotations

from .types import ASSIGNED_ENGINEER, FOUNDER, NEW_RECORD, TransitionRow, concat, rows

ENTITY = "solution_architecture_version"

STATUSES: tuple[str, ...] = ("draft", "confirmed")

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "draft", ("Agent_Runtime Job", ASSIGNED_ENGINEER, FOUNDER),
         ("graph_schema_valid", "non_empty_rationale_per_stack_item_and_decision"), 3),
    rows(ENTITY, "draft", "confirmed", (ASSIGNED_ENGINEER, FOUNDER), (), 3),
)
