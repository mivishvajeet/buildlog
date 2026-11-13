from fastapi.testclient import TestClient

from app.core.database import get_db
from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "buildlog-api"}


def test_readiness_check_when_database_is_available() -> None:
    class FakeSession:
        def execute(self, statement):
            return 1

    app.dependency_overrides[get_db] = lambda: FakeSession()
    try:
        response = client.get("/api/v1/health/ready")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "database": "ok"}
