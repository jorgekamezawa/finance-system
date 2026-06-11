from fastapi.testclient import TestClient

from app.config import Settings
from app.health import ReadinessCheck, get_readiness_check
from app.main import create_app


class FakeReadiness:
    def __init__(self, *, ready: bool) -> None:
        self._ready = ready

    async def database_is_ready(self) -> bool:
        return self._ready


def make_client(readiness: ReadinessCheck) -> TestClient:
    app = create_app(Settings(database_url="postgresql://unused"))
    app.dependency_overrides[get_readiness_check] = lambda: readiness
    return TestClient(app)


def test_health_returns_ok_when_database_is_ready() -> None:
    response = make_client(FakeReadiness(ready=True)).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "checks": {"db": "ok"}}


def test_health_returns_degraded_when_database_is_down() -> None:
    response = make_client(FakeReadiness(ready=False)).get("/health")

    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "checks": {"db": "down"}}
