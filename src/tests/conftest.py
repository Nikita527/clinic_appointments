from typing import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.core.auth import get_current_user
from src.main import app
from src.models.doctor import Doctor


@pytest.fixture(autouse=True, scope="session")
def override_get_current_user() -> Generator[None, None, None]:
    """Переопределение зависимости get_current_user."""

    async def fake_user() -> object:
        """Фейковый пользователь."""

        class User:
            id = 1
            email = "test@example.com"

        return User()

    app.dependency_overrides[get_current_user] = fake_user
    yield
    app.dependency_overrides = {}


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """Клиент для тестирования."""
    with TestClient(app) as ac:
        yield ac


@pytest.fixture
def test_user(client: TestClient) -> dict[str, str]:
    """Создание тестового пользователя."""
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": f"testuser_{uuid4()}@example.com",
        "password": "testpassword",
    }
    resp = client.post("/api/v1/auth/register", json=user_data)
    assert resp.status_code == 200
    user_id = resp.json()["id"]
    return {"id": user_id, "email": user_data["email"]}


@pytest.fixture
def test_doctor(client: TestClient) -> Doctor:
    """Создание тестового врача."""
    doctor_data = {
        "first_name": "Doc",
        "last_name": f"Test{uuid4()}",
        "specialization": "Терапевт",
    }
    resp = client.post("/api/v1/doctors/create", json=doctor_data)
    assert resp.status_code == 201
    return type("Doctor", (), {"id": resp.json()["id"]})()
