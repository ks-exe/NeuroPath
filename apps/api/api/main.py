"""FastAPI application factory."""

from fastapi import APIRouter, FastAPI

from api import public_inquiries
from api.errors import install_error_handling
from core.logging import configure_logging

API_PREFIX = "/api/v1"


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="NEUROPATH API", version="0.1.0")
    install_error_handling(app)

    router = APIRouter(prefix=API_PREFIX)

    @router.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    router.include_router(public_inquiries.router)
    app.include_router(router)
    return app


app = create_app()
