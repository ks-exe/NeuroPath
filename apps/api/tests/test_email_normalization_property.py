"""Property-based tests for email normalization (core/email.py)."""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from core.email import email_hash, normalize_email

# Property 16: Email normalization idempotence / Validates: Requirements 22.10

_WHITESPACE = st.text(alphabet=" \t\n\r\x0b\x0c\u00a0\u2003", max_size=5)


@st.composite
def _email_variants(draw: st.DrawFn) -> tuple[str, str]:
    """Return (base_email, variant); variant differs only in case and surrounding whitespace."""
    local = draw(st.from_regex(r"[a-z0-9][a-z0-9._+-]{0,20}", fullmatch=True))
    domain = draw(st.from_regex(r"[a-z0-9]{1,15}\.[a-z]{2,6}", fullmatch=True))
    base = f"{local}@{domain}"
    flips = draw(st.lists(st.booleans(), min_size=len(base), max_size=len(base)))
    mixed = "".join(c.upper() if f else c for c, f in zip(base, flips, strict=True))
    variant = draw(_WHITESPACE) + mixed + draw(_WHITESPACE)
    return base, variant


@settings(max_examples=200)
@given(st.text())
def test_normalize_is_idempotent_for_arbitrary_text(value: str) -> None:
    once = normalize_email(value)
    assert normalize_email(once) == once


@settings(max_examples=200)
@given(_email_variants())
def test_normalize_is_idempotent_for_email_like_strings(pair: tuple[str, str]) -> None:
    _, variant = pair
    once = normalize_email(variant)
    assert normalize_email(once) == once


@settings(max_examples=200)
@given(st.text())
def test_normalized_output_is_trimmed_and_lowercase(value: str) -> None:
    out = normalize_email(value)
    assert out == out.strip()
    assert out == out.lower()


@settings(max_examples=200)
@given(_email_variants(), _email_variants())
def test_case_and_whitespace_variants_share_hash(
    pair: tuple[str, str], other: tuple[str, str]
) -> None:
    base, variant = pair
    assert normalize_email(variant) == base
    assert email_hash(normalize_email(variant)) == email_hash(normalize_email(base))
    # Distinct normalized emails must not collide.
    if other[0] != base:
        assert email_hash(normalize_email(other[1])) != email_hash(base)
