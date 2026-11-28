"""Error codes and the typed exception services raise (R19.3, design "Error Code Catalogue").

Clients branch on ``code``, never on ``message``. One handler in ``api.errors`` maps every
exception to an HTTP status and the ``ErrorEnvelope``; no router builds an error body by hand.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

VALIDATION_FAILED: Final = "validation_failed"
UNAUTHENTICATED: Final = "unauthenticated"
FORBIDDEN: Final = "forbidden"
NOT_FOUND: Final = "not_found"
METHOD_NOT_ALLOWED: Final = "method_not_allowed"
INVALID_TRANSITION: Final = "invalid_transition"
GUARD_FAILED: Final = "guard_failed"
CONFLICT_STATE: Final = "conflict_state"
RATE_LIMITED: Final = "rate_limited"
DAILY_COST_LIMIT: Final = "daily_cost_limit"
AUDIT_WRITE_FAILED: Final = "audit_write_failed"
INTERNAL_ERROR: Final = "internal_error"
DEPENDENCY_UNAVAILABLE: Final = "dependency_unavailable"
# Not in the design catalogue: framework HTTP errors with any other status (e.g. 400).
HTTP_ERROR: Final = "http_error"

# Default HTTP status per code.
CODE_STATUS: Final[dict[str, int]] = {
    VALIDATION_FAILED: 422,
    UNAUTHENTICATED: 401,
    FORBIDDEN: 403,
    NOT_FOUND: 404,
    METHOD_NOT_ALLOWED: 405,
    INVALID_TRANSITION: 409,
    GUARD_FAILED: 409,
    CONFLICT_STATE: 409,
    RATE_LIMITED: 429,
    DAILY_COST_LIMIT: 429,
    AUDIT_WRITE_FAILED: 500,
    INTERNAL_ERROR: 500,
    DEPENDENCY_UNAVAILABLE: 503,
}

# Code used when the framework raises an HTTP error with this status.
STATUS_CODE: Final[dict[int, str]] = {
    401: UNAUTHENTICATED,
    403: FORBIDDEN,
    404: NOT_FOUND,
    405: METHOD_NOT_ALLOWED,
    409: CONFLICT_STATE,
    422: VALIDATION_FAILED,
    429: RATE_LIMITED,
    500: INTERNAL_ERROR,
    503: DEPENDENCY_UNAVAILABLE,
}

# Fixed messages. 404 is identical for missing, foreign, and hidden resources (R18.2).
DEFAULT_MESSAGES: Final[dict[str, str]] = {
    VALIDATION_FAILED: "The request is invalid.",
    UNAUTHENTICATED: "Authentication is required.",
    FORBIDDEN: "You do not have permission to perform this action.",
    NOT_FOUND: "The requested resource was not found.",
    METHOD_NOT_ALLOWED: "This method is not allowed for this resource.",
    CONFLICT_STATE: "The operation is not valid in the current state.",
    RATE_LIMITED: "Too many requests. Retry later.",
    INTERNAL_ERROR: "An internal error occurred.",
    DEPENDENCY_UNAVAILABLE: "A required service is unavailable.",
    HTTP_ERROR: "The request could not be processed.",
}


class ApiError(Exception):
    """A domain error mapped to an HTTP status and the error envelope.

    ``fields`` is a sequence of ``(field, message)`` pairs and is empty unless the error is a
    validation error. ``message`` must be safe to show the caller.
    """

    def __init__(
        self,
        code: str,
        message: str | None = None,
        *,
        status: int | None = None,
        fields: Sequence[tuple[str, str]] = (),
        headers: dict[str, str] | None = None,
    ) -> None:
        self.code = code
        self.message = message or DEFAULT_MESSAGES.get(code, DEFAULT_MESSAGES[HTTP_ERROR])
        self.status = status if status is not None else CODE_STATUS.get(code, 400)
        self.fields = list(fields)
        self.headers = headers
        super().__init__(f"{self.code}: {self.message}")
