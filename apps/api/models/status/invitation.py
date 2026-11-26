"""Invitation status model (Appendix A.2.4)."""

from __future__ import annotations

from .types import (
    AUTHORIZED_REVIEWER,
    CLIENT_OWNER,
    NEW_RECORD,
    SYSTEM,
    TransitionRow,
    concat,
    rows,
)

ENTITY = "invitation"

STATUSES: tuple[str, ...] = ("pending", "accepted", "expired", "revoked")
TERMINAL_STATUSES: frozenset[str] = frozenset({"accepted", "expired", "revoked"})

TRANSITIONS: tuple[TransitionRow, ...] = concat(
    rows(ENTITY, NEW_RECORD, "pending", (AUTHORIZED_REVIEWER, CLIENT_OWNER),
         ("bound_to_normalized_email_and_one_organization", "expiry_set_from_configured_period",
          "client_owner_own_organization_only_else_404"), 2),
    rows(ENTITY, "pending", "accepted", (SYSTEM,),
         ("not_expired_revoked_or_used", "registering_email_matches_after_normalization"), 2),
    rows(ENTITY, "pending", "expired", (SYSTEM,), ("expiry_time_reached",), 2),
    rows(ENTITY, "pending", "revoked", (AUTHORIZED_REVIEWER, "Issuing " + CLIENT_OWNER),
         ("not_accepted",), 2),
)
