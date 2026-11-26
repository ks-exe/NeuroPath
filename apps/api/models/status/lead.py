"""Lead status model (Appendix A.2.1)."""

from __future__ import annotations

from .types import (
    ADMINISTRATOR,
    AUTHORIZED_REVIEWER,
    FOUNDER,
    INTERNAL_AGENT,
    NEW_RECORD,
    PROJECT_MANAGER,
    SYSTEM,
    TransitionRow,
    concat,
    rows,
)

ENTITY = "lead"

STATUSES: tuple[str, ...] = ("New", "Contacted", "Converted", "Disqualified", "Opted Out", "Merged")
TERMINAL_STATUSES: frozenset[str] = frozenset({"Opted Out", "Merged"})  # no outgoing transition

_NOT_MERGED = tuple(s for s in STATUSES if s != "Merged")
_STAFF = (FOUNDER, ADMINISTRATOR, PROJECT_MANAGER)

# Phase: leads status columns are created in Phase 2 (Appendix B).
TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "New", (SYSTEM, "Lead Research " + INTERNAL_AGENT),
         ("source_recorded_for_each_data_item",), 2),
    rows(ENTITY, "New", "Contacted", _STAFF,
         ("email_not_on_opt_out_list", "external_email_only_through_founder_approved_path"), 2),
    rows(ENTITY, ("New", "Contacted"), "Converted", (SYSTEM,),
         ("invitation_bound_to_lead_email_accepted",), 2),
    rows(ENTITY, ("New", "Contacted"), "Disqualified", _STAFF, ("non_empty_reason",), 2),
    rows(ENTITY, _NOT_MERGED, "Opted Out", (SYSTEM,),
         ("normalized_email_added_to_opt_out_list",), 2),
    rows(ENTITY, _NOT_MERGED, "Merged", (AUTHORIZED_REVIEWER,),
         ("both_leads_flagged_possible_duplicates", "sources_and_consents_preserved"), 2),
)
