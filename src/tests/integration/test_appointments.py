from datetime import datetime, timedelta, timezone

from dateutil.parser import isoparse
from fastapi.testclient import TestClient

from src.main import app
from src.models.doctor import Doctor

client = TestClient(app)


def test_create_and_get_appointment(
    client: TestClient, test_user: dict[str, str], test_doctor: Doctor
) -> None:
    """Проверка создания и получения записи к врачу."""
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    start_time = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(minutes=30)
    payload = {
        "doctor_id": test_doctor.id,
        "user_id": test_user.get("id"),
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }

    resp = client.post("/api/v1/appointments", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    appointment_id = data["id"]

    resp2 = client.get(f"/api/v1/appointments/{appointment_id}")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["doctor_id"] == payload["doctor_id"]
    assert isoparse(str(data2["start_time"])) == isoparse(
        str(payload["start_time"])
    )


def test_cannot_create_in_past(
    client: TestClient, test_doctor: Doctor, test_user: dict[str, str]
) -> None:
    """Проверка запрета создания записи в прошлом."""
    past = datetime.now(timezone.utc) - timedelta(days=1)
    start_time = past.replace(hour=12, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(minutes=30)
    payload = {
        "doctor_id": test_doctor.id,
        "user_id": test_user.get("id"),
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    resp = client.post("/api/v1/appointments", json=payload)
    assert resp.status_code == 400


def test_cannot_create_with_end_before_start(
    client: TestClient, test_doctor: Doctor, test_user: dict[str, str]
) -> None:
    """Проверка запрета создания записи с концом раньше начала."""
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    start_time = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0)
    end_time = start_time - timedelta(minutes=30)
    payload = {
        "doctor_id": test_doctor.id,
        "user_id": test_user.get("id"),
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    resp = client.post("/api/v1/appointments", json=payload)
    assert resp.status_code == 400
