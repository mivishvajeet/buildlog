import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.main import app
from app.models import Base

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


def test_register_login_and_read_current_user(client: TestClient) -> None:
    registration = client.post(
        "/api/v1/auth/register",
        json={
            "email": "  ENGINEER@example.com ",
            "display_name": "  Buildlog User  ",
            "password": "a-long-test-password",
        },
    )

    assert registration.status_code == 201
    user = registration.json()
    assert user["email"] == "engineer@example.com"
    assert user["display_name"] == "Buildlog User"
    assert "password_hash" not in user
    assert "password" not in user

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "ENGINEER@example.com", "password": "a-long-test-password"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    assert login.json()["token_type"] == "bearer"

    current_user = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert current_user.status_code == 200
    assert current_user.json()["id"] == user["id"]


def test_registration_rejects_duplicate_email(client: TestClient) -> None:
    payload = {
        "email": "engineer@example.com",
        "display_name": "Buildlog User",
        "password": "a-long-test-password",
    }
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    duplicate = client.post("/api/v1/auth/register", json=payload)
    assert duplicate.status_code == 409


def test_current_user_requires_valid_token(client: TestClient) -> None:
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

    invalid_token = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer not-a-valid-token"},
    )
    assert invalid_token.status_code == 401


def test_registration_requires_strong_password(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "engineer@example.com",
            "display_name": "Buildlog User",
            "password": "short",
        },
    )
    assert response.status_code == 422
