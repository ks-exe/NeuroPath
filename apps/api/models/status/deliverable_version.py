"""Deliverable version status model (Appendix A.2.13)."""

from __future__ import annotations

from .types import (
    CLIENT_MEMBER,
    CLIENT_OWNER,
    FOUNDER,
    NEW_RECORD,
    STAFF_ASSIGNED,
    TransitionRow,
    concat,
    rows,
)

ENTITY = "deliverable_version"

STATUSES: tuple[str, ...] = ("draft", "Approved for Client", "Accepted", "Rejected")

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "draft", (STAFF_ASSIGNED,),
         ("file_stored_and_available", "source_code_reference_has_url_and_commit_or_tag_without_credentials"), 4),
    rows(ENTITY, "draft", "Approved for Client", ("Holder of Deliverable approval permission",), (), 4),
    rows(ENTITY, "Approved for Client", "Accepted", (CLIENT_OWNER, CLIENT_MEMBER, FOUNDER),
         ("client_member_has_decision_permission", "founder_off_platform_with_evidence",
          "create_acceptance_record"), 4),
    rows(ENTITY, "Approved for Client", "Rejected", (CLIENT_OWNER, CLIENT_MEMBER),
         ("client_member_has_decision_permission", "non_empty_reason_in_acceptance_record"), 4),
)
