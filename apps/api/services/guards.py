"""Guard registry for the Status Transition Engine (R8.3, R8.6).

Guards are pure functions ``(GuardContext) -> (passed, reason)``. They do no I/O.
They read only the loaded state carried by the context.

Every guard name used by an Appendix A row (``TRANSITION_TABLES``) is registered:

* **Predicate guards** with dedicated logic (``non_empty_reason``, ...).
* **Fact guards**: the generic form. The guard passes only when the service
  that loaded the entity supplied ``facts[name] is True``. A missing fact fails
  closed with a named reason, so a guard whose data is unavailable never passes.
* **Effect names**: Appendix A also lists follow-up actions in the guard column
  (``store_prior_status_and_reason``, ``send_notification``, ...). They are not
  predicates. They always pass and are reported on the result for the owning
  service to perform in the same transaction.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

GuardResult = tuple[bool, str | None]


@dataclass(frozen=True)
class GuardContext:
    entity_type: str
    from_status: str | None
    target: str
    reason: str | None
    is_human: bool
    prior_status: str | None = None
    facts: Mapping[str, Any] = field(default_factory=dict)


Guard = Callable[[GuardContext], GuardResult]


@dataclass(frozen=True)
class GuardSpec:
    name: str
    fn: Guard
    # First phase in which the guard's entity is delivered. Rows using the guard
    # are disabled below this phase (R8.6).
    min_phase: int = 1
    is_effect: bool = False


GUARD_REGISTRY: dict[str, GuardSpec] = {}

# Follow-up actions and response annotations that Appendix A lists as guards.
EFFECT_NAMES: frozenset[str] = frozenset(
    {
        "audit_log_on_guard_failure",
        "both_leads_flagged_possible_duplicates",
        "compute_delivery_reference_and_hash",
        "create_acceptance_record",
        "create_new_scope_baseline_version_referencing_change_request",
        "create_scope_baseline_v1_on_success",
        "dead_letter_record_and_notification",
        "delete_object",
        "delete_stored_object",
        "expiry_set_from_configured_period",
        "guest_request_401",
        "inquiry_questions_opened_in_same_request",
        "internal_agent_request_403_and_audit",
        "normalized_email_added_to_opt_out_list",
        "other_roles_receive_403",
        "quarantine_reason_scanner_unavailable",
        "record_confirming_user_and_timestamp",
        "recording_user_and_time_stored",
        "send_internal_notification",
        "send_notification",
        "sources_and_consents_preserved",
        "store_content_hash_and_freeze_content",
        "store_prior_status_and_reason",
        "system_on_client_comment",
        "technical_assessment_created_in_same_request",
    }
)


def _register(spec: GuardSpec) -> None:
    GUARD_REGISTRY[spec.name] = spec


def guard(name: str, *, min_phase: int = 1) -> Callable[[Guard], Guard]:
    """Register a predicate guard under ``name``."""

    def deco(fn: Guard) -> Guard:
        _register(GuardSpec(name, fn, min_phase))
        return fn

    return deco


def fact_guard(name: str, *, min_phase: int = 1) -> GuardSpec:
    """Build a fail-closed guard that reads ``facts[name]``."""

    def fn(ctx: GuardContext) -> GuardResult:
        if name not in ctx.facts:
            return False, f"Guard '{name}' cannot be evaluated: context data is unavailable"
        if ctx.facts[name] is True:
            return True, None
        return False, f"Guard '{name}' failed"

    return GuardSpec(name, fn, min_phase)


def _effect(name: str) -> GuardSpec:
    return GuardSpec(name, lambda _ctx: (True, None), is_effect=True)


@guard("non_empty_reason")
def non_empty_reason(ctx: GuardContext) -> GuardResult:
    if ctx.reason is not None and ctx.reason.strip():
        return True, None
    return False, "Guard 'non_empty_reason' failed: a reason is required"


def _human_only(name: str) -> Guard:
    def fn(ctx: GuardContext) -> GuardResult:
        if ctx.is_human:
            return True, None
        return False, f"Guard '{name}' failed: only a human principal may do this"

    return fn


for _n in ("human_principal_only", "human_principal_only_else_403_and_audit"):
    _register(GuardSpec(_n, _human_only(_n)))


@guard("target_equals_stored_prior_status")
def target_equals_stored_prior_status(ctx: GuardContext) -> GuardResult:
    if ctx.prior_status is None:
        return False, (
            "Guard 'target_equals_stored_prior_status' cannot be evaluated: "
            "no stored prior status"
        )
    if ctx.target == ctx.prior_status:
        return True, None
    return False, (
        "Guard 'target_equals_stored_prior_status' failed: "
        f"stored prior status is '{ctx.prior_status}'"
    )


@guard("agreement_in_effect", min_phase=4)
def agreement_in_effect(ctx: GuardContext) -> GuardResult:
    status = ctx.facts.get("agreement_status")
    if status is None:
        return False, (
            "Guard 'agreement_in_effect' cannot be evaluated: Agreement state is unavailable"
        )
    if status == "In Effect":
        return True, None
    return False, "Guard 'agreement_in_effect' failed: the Agreement is not In Effect"


def register_all_table_guards() -> None:
    """Register every guard name found in the transition tables (idempotent)."""
    from models.status import TRANSITION_TABLES

    names = {g for rs in TRANSITION_TABLES.values() for r in rs for g in r.guards}
    for name in sorted(names - GUARD_REGISTRY.keys()):
        _register(_effect(name) if name in EFFECT_NAMES else fact_guard(name))


register_all_table_guards()


def evaluate(name: str, ctx: GuardContext) -> GuardResult:
    """Evaluate one guard. An unregistered name fails closed."""
    spec = GUARD_REGISTRY.get(name)
    if spec is None:
        return False, f"Guard '{name}' is not registered"
    return spec.fn(ctx)
