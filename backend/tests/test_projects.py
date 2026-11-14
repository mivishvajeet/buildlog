import pytest
from app.core.database import get_db
from app.main import app
from app.models import Base
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def register_and_login(client: TestClient, email: str) -> str:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "display_name": "Project Tester",
            "password": "a-long-test-password",
        },
    )
    assert response.status_code == 201
    login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "a-long-test-password"},
    )
    assert login.status_code == 200
    return login.json()["access_token"]


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_project_crud_and_slug_collision(client: TestClient) -> None:
    token = register_and_login(client, "owner@example.com")
    headers = auth(token)

    created = client.post(
        "/api/v1/projects",
        headers=headers,
        json={
            "name": "Airlytics",
            "category": "Data Engineering",
            "description": "Flight tracking analytics",
            "status": "active",
            "started_on": "2026-11-01",
            "target_date": "2027-01-01",
        },
    )
    assert created.status_code == 201
    project = created.json()
    assert project["name"] == "Airlytics"
    assert project["slug"] == "airlytics"
    assert project["visibility"] == "private"

    duplicate_name = client.post(
        "/api/v1/projects",
        headers=headers,
        json={"name": "Airlytics"},
    )
    assert duplicate_name.status_code == 201
    assert duplicate_name.json()["slug"] == "airlytics-2"

    listed = client.get("/api/v1/projects", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 2

    fetched = client.get(f"/api/v1/projects/{project['id']}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["id"] == project["id"]

    updated = client.patch(
        f"/api/v1/projects/{project['id']}",
        headers=headers,
        json={"name": "Airlytics Platform", "status": "completed"},
    )
    assert updated.status_code == 200
    assert updated.json()["slug"] == "airlytics-platform"
    assert updated.json()["status"] == "completed"
    assert updated.json()["completed_at"] is not None

    deleted = client.delete(f"/api/v1/projects/{project['id']}", headers=headers)
    assert deleted.status_code == 204
    missing = client.get(f"/api/v1/projects/{project['id']}", headers=headers)
    assert missing.status_code == 404


def test_project_endpoints_require_authentication(client: TestClient) -> None:
    response = client.get("/api/v1/projects")
    assert response.status_code == 401


def test_users_cannot_access_each_others_projects(client: TestClient) -> None:
    owner_token = register_and_login(client, "owner@example.com")
    other_token = register_and_login(client, "other@example.com")

    created = client.post(
        "/api/v1/projects",
        headers=auth(owner_token),
        json={"name": "Private Project"},
    )
    project_id = created.json()["id"]

    assert client.get(
        f"/api/v1/projects/{project_id}", headers=auth(other_token)
    ).status_code == 404
    assert client.patch(
        f"/api/v1/projects/{project_id}",
        headers=auth(other_token),
        json={"name": "Hijacked"},
    ).status_code == 404
    assert client.delete(
        f"/api/v1/projects/{project_id}", headers=auth(other_token)
    ).status_code == 404

    other_projects = client.get("/api/v1/projects", headers=auth(other_token))
    assert other_projects.status_code == 200
    assert other_projects.json() == []


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "   "},
        {"name": "Invalid dates", "started_on": "2026-12-01", "target_date": "2026-11-01"},
        {"name": "Bad status", "status": "started"},
    ],
)
def test_project_creation_validates_payload(client: TestClient, payload: dict) -> None:
    token = register_and_login(client, "validation@example.com")
    response = client.post("/api/v1/projects", headers=auth(token), json=payload)
    assert response.status_code == 422



def test_project_patch_rejects_empty_or_null_required_fields(client: TestClient) -> None:
    token = register_and_login(client, "patch-validation@example.com")
    headers = auth(token)
    created = client.post(
        "/api/v1/projects", headers=headers, json={"name": "Patch Validation"}
    )
    project_id = created.json()["id"]

    assert client.patch(
        f"/api/v1/projects/{project_id}", headers=headers, json={}
    ).status_code == 422
    assert client.patch(
        f"/api/v1/projects/{project_id}", headers=headers, json={"status": None}
    ).status_code == 422
    assert client.patch(
        f"/api/v1/projects/{project_id}", headers=headers, json={"name": None}
    ).status_code == 422
