from fastapi.testclient import TestClient

from api.main import create_app


def test_health_returns_ok() -> None:
    client = TestClient(create_app())
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_only_health_route_is_registered() -> None:
    paths = {r.path for r in create_app().routes if r.path.startswith("/api/")}  # type: ignore[attr-defined]
    assert paths == {"/api/v1/health"}
