"""Base for update schemas: status fields are excluded (R8.5).

Statuses change only through ``services.transitions.transition``.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

STATUS_FIELD_NAMES = frozenset({"status", "prior_status", "stored_prior_status"})


class UpdateSchema(BaseModel):
    """Base class for update payloads. Declaring a status field raises TypeError.

    Unknown input keys, including ``status``, are rejected with a validation error.
    """

    model_config = ConfigDict(extra="forbid")

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        bad = STATUS_FIELD_NAMES & cls.model_fields.keys()
        if bad:
            raise TypeError(
                f"{cls.__name__} must not declare status fields {sorted(bad)}; use transition()"
            )
