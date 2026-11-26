"""FastAPI application factory."""

from fastapi import APIRouter, FastAPI

API_PREFIX = "/api/v1"


def create_app() -> FastAPI:
    app = FastAPI(title="NEUROPATH API", version="0.1.0")

    router = APIRouter(prefix=API_PREFIX)

    @router.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(router)
    return app


app = create_app()
