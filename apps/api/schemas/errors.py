"""Error envelope returned by every error response (R19.2, R19.3)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FieldError(BaseModel):
    field: str
    message: str


class ErrorEnvelope(BaseModel):
    code: str
    message: str
    fields: list[FieldError] = Field(default_factory=list)
    request_id: str
