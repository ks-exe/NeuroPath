"""Request id context and JSON logging (R19.4).

Every log line is one JSON object carrying the request id of the current request. Request
bodies and Authorization or Cookie headers are never logged.
"""

from __future__ import annotations

import json
import logging
import re
import sys
import uuid
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any

REQUEST_ID_HEADER = "X-Request-ID"
_REQUEST_ID_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")

request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)

# Extra keys that are never written, whatever a caller passes in ``extra``.
_REDACTED_KEYS = frozenset(
    {"authorization", "cookie", "set-cookie", "set_cookie", "body", "request_body", "password"}
)
_STANDARD_ATTRS = frozenset(
    logging.LogRecord("", 0, "", 0, "", None, None).__dict__.keys() | {"message", "asctime"}
)
_HANDLER_MARK = "_neuropath_json_handler"


def resolve_request_id(incoming: str | None) -> str:
    """Accept a safe incoming id (<= 64 chars of [A-Za-z0-9._-]); otherwise generate a UUID4."""
    if incoming and _REQUEST_ID_RE.fullmatch(incoming):
        return incoming
    return str(uuid.uuid4())


def get_request_id() -> str | None:
    return request_id_var.get()


class JsonFormatter(logging.Formatter):
    """One JSON object per line: timestamp, level, logger, message, request_id, extras."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", None) or request_id_var.get(),
        }
        for key, value in record.__dict__.items():
            if key in _STANDARD_ATTRS or key in payload or key.startswith("_"):
                continue
            if key.lower() in _REDACTED_KEYS:
                continue
            payload[key] = value
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def _install_record_factory() -> None:
    """Stamp the current request id on each record when it is created, so handlers that
    format later (queues, test capture) still see it."""
    current = logging.getLogRecordFactory()
    if getattr(current, _HANDLER_MARK, False):
        return

    def factory(*args: Any, **kwargs: Any) -> logging.LogRecord:
        record = current(*args, **kwargs)
        if getattr(record, "request_id", None) is None:
            record.request_id = request_id_var.get()
        return record

    setattr(factory, _HANDLER_MARK, True)
    logging.setLogRecordFactory(factory)


def configure_logging(level: int = logging.INFO) -> None:
    """Install the JSON handler on the root logger. Calling it again has no effect."""
    _install_record_factory()
    root = logging.getLogger()
    if any(getattr(h, _HANDLER_MARK, False) for h in root.handlers):
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    setattr(handler, _HANDLER_MARK, True)
    root.addHandler(handler)
    root.setLevel(level)
