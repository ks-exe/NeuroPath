"""Property test for the Status Transition Engine (design Property 6, R8.7).

The oracle below computes the expected outcome from the Appendix A rows and
the documented guard semantics. It does not call the engine's helpers.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from hypothesis import given, settings
from hypothesis import strategies as st

from models.status import NEW_RECORD, PRIOR_STATUS, STATUS_SETS, TRANSITION_TABLES, TransitionRow
from services.guards import EFFECT_NAMES, GUARD_REGISTRY
from services.transitions import AuditEntry, transition

ENTITIES = sorted(TRANSITION_TABLES)
ALL_ROLES = sorted(
    {role for rs in TRANSITION_TABLES.values() for r in rs for role in r.allowed_roles}
)
UNKNOWN_ROLE = "Guest"
PHASES = list(range(0, 6))
_MISSING = object()


@dataclass
class FakeEntity:
    entity_type: str
    status: str | None
    prior_status: str | None
    facts: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FakePrincipal:
    roles: frozenset[str]
    is_human: bool


# --- independent oracle ------------------------------------------------------


def _guard_passes(name: str, target: str, reason: str | None, is_human: bool,
                  prior: str | None, facts: Mapping[str, Any]) -> bool:
    if name in EFFECT_NAMES:
        return True
    if name == "non_empty_reason":
        return reason is not None and reason.strip() != ""
    if name in ("human_principal_only", "human_principal_only_else_403_and_audit"):
        return is_human
    if name == "target_equals_stored_prior_status":
        return prior is not None and target == prior
    if name == "agreement_in_effect":
        return facts.get("agreement_status") == "In Effect"
    return facts.get(name) is True  # fact guards fail closed


def _expected_accept(entity_type: str, src: str, target: str, role: str, phase: int,
                     reason: str | None, is_human: bool, prior: str | None,
                     facts: Mapping[str, Any]) -> bool:
    for row in TRANSITION_TABLES[entity_type]:
        if row.from_status != src:
            continue
        if row.to_status == PRIOR_STATUS:
            if prior is None or target != prior:
                continue
        elif row.to_status != target:
            continue
        if row.enabled_phase > phase:
            continue
        if any(GUARD_REGISTRY[g].min_phase > phase for g in row.guards):
            continue
        if role not in row.allowed_roles:
            continue
        if all(_guard_passes(g, target, reason, is_human, prior, facts) for g in row.guards):
            return True
    return False


# --- strategies --------------------------------------------------------------


@st.composite
def scenarios(draw: st.DrawFn) -> dict[str, Any]:
    entity_type = draw(st.sampled_from(ENTITIES))
    table = TRANSITION_TABLES[entity_type]
    statuses = list(STATUS_SETS[entity_type])
    prior = draw(st.none() | st.sampled_from(statuses))

    if table and draw(st.booleans()):
        # Bias towards a defined row so acceptance is exercised often.
        row: TransitionRow = draw(st.sampled_from(table))
        src = row.from_status
        target = prior if (row.to_status == PRIOR_STATUS and prior) else row.to_status
        if target == PRIOR_STATUS:
            target = draw(st.sampled_from(statuses))
        role = draw(st.sampled_from(sorted(row.allowed_roles)) | st.sampled_from(ALL_ROLES))
    else:
        src = draw(st.sampled_from([NEW_RECORD, *statuses]))
        target = draw(st.sampled_from(statuses))
        role = draw(st.sampled_from([*ALL_ROLES, UNKNOWN_ROLE]))

    guard_names = sorted({g for r in table for g in r.guards})
    facts: dict[str, Any] = {}
    for name in guard_names:
        value = draw(st.sampled_from([True, True, True, False, _MISSING]))
        if value is not _MISSING:
            facts[name] = value
    agreement = draw(st.sampled_from([None, "In Effect", "Draft"]))
    if agreement is not None:
        facts["agreement_status"] = agreement
    phase = draw(st.sampled_from(PHASES))
    reason = draw(st.sampled_from([None, "", "   ", "client asked"]))
    is_human = draw(st.booleans())

    if draw(st.booleans()):
        # Make the context permissive so that a matching row usually passes.
        phase = max(PHASES)
        reason = "client asked"
        is_human = True
        facts = {name: True for name in guard_names} | {"agreement_status": "In Effect"}

    return {
        "entity_type": entity_type,
        "src": src,
        "target": target,
        "role": role,
        "phase": phase,
        "reason": reason,
        "is_human": is_human,
        "prior": prior,
        "facts": facts,
    }


# Property 6: Status transition validity / Validates: Requirements 8.7
@settings(max_examples=300, deadline=None)
@given(scenarios())
def test_transition_accepted_iff_matching_enabled_row(sc: dict[str, Any]) -> None:
    status = None if sc["src"] == NEW_RECORD else sc["src"]
    entity = FakeEntity(sc["entity_type"], status, sc["prior"], sc["facts"])
    principal = FakePrincipal(frozenset({sc["role"]}), sc["is_human"])
    calls: list[AuditEntry] = []

    result = transition(entity, sc["target"], principal, sc["reason"],
                        audit_hook=calls.append, platform_phase=sc["phase"])

    expected = _expected_accept(sc["entity_type"], sc["src"], sc["target"], sc["role"],
                                sc["phase"], sc["reason"], sc["is_human"], sc["prior"],
                                sc["facts"])
    assert result.accepted is expected
    if expected:
        assert result.rejection is None
        assert entity.status == sc["target"]
        assert len(calls) == 1
        assert calls[0].prior_status == status and calls[0].new_status == sc["target"]
    else:
        assert result.rejection is not None
        assert entity.status == status
        assert entity.prior_status == sc["prior"]
        assert calls == []


# --- example-based checks ----------------------------------------------------


def test_rejected_transition_leaves_status_and_skips_hook() -> None:
    entity = FakeEntity("lead", "New", None, {})
    calls: list[AuditEntry] = []
    result = transition(entity, "Disqualified", FakePrincipal(frozenset({"Founder"}), True),
                        reason="", audit_hook=calls.append, platform_phase=2)
    assert not result.accepted
    assert result.rejection is not None and result.rejection.kind == "guard_failed"
    assert result.rejection.guard == "non_empty_reason"
    assert entity.status == "New"
    assert calls == []


def test_accepted_transition_calls_hook_once() -> None:
    entity = FakeEntity("lead", "New", None, {})
    calls: list[AuditEntry] = []
    result = transition(entity, "Disqualified", FakePrincipal(frozenset({"Founder"}), True),
                        reason="duplicate", audit_hook=calls.append, platform_phase=2)
    assert result.accepted
    assert entity.status == "Disqualified"
    assert len(calls) == 1
    assert calls[0].prior_status == "New" and calls[0].reason == "duplicate"


def test_row_disabled_before_its_phase() -> None:
    entity = FakeEntity("lead", "New", None, {})
    calls: list[AuditEntry] = []
    result = transition(entity, "Disqualified", FakePrincipal(frozenset({"Founder"}), True),
                        reason="duplicate", audit_hook=calls.append, platform_phase=1)
    assert result.rejection is not None and result.rejection.kind == "disabled_status"
    assert entity.status == "New" and calls == []
