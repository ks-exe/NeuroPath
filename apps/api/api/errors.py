"""Request id middleware and exception handlers producing the ErrorEnvelope (R19.2-R19.4)."""

from __future__ import annotations

import logging
import time
from collections.abc import Mapping, Sequence
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from core import errors
from core.logging import REQUEST_ID_HEADER, get_request_id, request_id_var, resolve_request_id
from schemas.errors import ErrorEnvelope, FieldError

logger = logging.getLogger("api")


def error_response(
    status: int,
    code: str,
    message: str,
    fields: Sequence[tuple[str, str]] = (),
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    request_id = get_request_id() or resolve_request_id(None)
    body = ErrorEnvelope(
        code=code,
        message=message,
        fields=[FieldError(field=f, message=m) for f, m in fields],
        request_id=request_id,
    )
    out_headers = dict(headers or {})
    out_headers[REQUEST_ID_HEADER] = request_id
    return JSONResponse(status_code=status, content=body.model_dump(), headers=out_headers)


class RequestIdMiddleware:
    """Assigns the request id, logs one access line, and turns unhandled errors into a 500.

    Pure ASGI so the context variable covers the whole request, including the error path.
    Only method, path, status and duration are logged: never bodies, query strings or headers.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        incoming: str | None = None
        for name, value in scope.get("headers", []):
            if name.lower() == b"x-request-id":
                incoming = value.decode("latin-1")
                break
        request_id = resolve_request_id(incoming)
        token = request_id_var.set(request_id)
        started = time.perf_counter()
        status_holder: dict[str, Any] = {"status": None}

        async def send_with_id(message: Message) -> None:
            if message["type"] == "http.response.start":
                status_holder["status"] = message["status"]
                headers = [
                    (k, v) for k, v in message.get("headers", []) if k.lower() != b"x-request-id"
                ]
                headers.append((b"x-request-id", request_id.encode("latin-1")))
                message["headers"] = headers
            await send(message)

        try:
            try:
                await self.app(scope, receive, send_with_id)
            except Exception:
                logger.exception(
                    "unhandled error", extra={"method": scope["method"], "path": scope["path"]}
                )
                if status_holder["status"] is not None:
                    raise
                response = error_response(
                    500, errors.INTERNAL_ERROR, errors.DEFAULT_MESSAGES[errors.INTERNAL_ERROR]
                )
                await response(scope, receive, send_with_id)
            logger.info(
                "request",
                extra={
                    "method": scope["method"],
                    "path": scope["path"],
                    "status": status_holder["status"],
                    "duration_ms": round((time.perf_counter() - started) * 1000, 2),
                },
            )
        finally:
            request_id_var.reset(token)


async def _api_error_handler(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, errors.ApiError)
    if exc.status >= 500:
        logger.error("api error", extra={"code": exc.code, "status": exc.status})
    return error_response(exc.status, exc.code, exc.message, exc.fields, exc.headers)


async def _http_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)
    code = errors.STATUS_CODE.get(exc.status_code, errors.HTTP_ERROR)
    message = errors.DEFAULT_MESSAGES.get(code, errors.DEFAULT_MESSAGES[errors.HTTP_ERROR])
    return error_response(exc.status_code, code, message, headers=exc.headers)


async def _validation_handler(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    fields = [
        (".".join(str(part) for part in err.get("loc", ())), str(err.get("msg", "invalid")))
        for err in exc.errors()
    ]
    return error_response(
        422,
        errors.VALIDATION_FAILED,
        errors.DEFAULT_MESSAGES[errors.VALIDATION_FAILED],
        fields,
    )


def install_error_handling(app: FastAPI) -> None:
    app.add_exception_handler(errors.ApiError, _api_error_handler)
    app.add_exception_handler(StarletteHTTPException, _http_exception_handler)
    app.add_exception_handler(RequestValidationError, _validation_handler)
    app.add_middleware(RequestIdMiddleware)
