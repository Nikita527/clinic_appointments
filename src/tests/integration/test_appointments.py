from datetime import datetime, timedelta, timezone

import pytest
from httpx import AsyncClient
from dateutil.parser import isoparse


@pytest.mark.asyncio
async def test_create_and_get_appointment(
    async_session, test_user_token, test_doctor
):
    """Проверка создания и получения записи к врачу."""
    headers = {"Authorization": f"Bearer {test_user_token}"}
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    start_time = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(minutes=30)
    payload = {
        "doctor_id": test_doctor.id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }

    async with AsyncClient(base_url="http://localhost:8000") as ac:
        resp = await ac.post(
            "/api/v1/appointments", json=payload, headers=headers
        )
        assert resp.status_code == 201
        data = resp.json()
        appointment_id = data["id"]

        resp2 = await ac.get(
            f"/api/v1/appointments/{appointment_id}", headers=headers
        )
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert data2["doctor_id"] == payload["doctor_id"]
        assert isoparse(data2["start_time"]) == isoparse(payload["start_time"])


@pytest.mark.asyncio
async def test_cannot_create_in_past(
    async_session, test_user_token, test_doctor
):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    past = datetime.now(timezone.utc) - timedelta(days=1)
    start_time = past.replace(hour=12, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(minutes=30)
    payload = {
        "doctor_id": test_doctor.id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        resp = await ac.post(
            "/api/v1/appointments", json=payload, headers=headers
        )
        assert resp.status_code == 400


@pytest.mark.asyncio
async def test_cannot_create_with_end_before_start(
    async_session, test_user_token, test_doctor
):
    headers = {"Authorization": f"Bearer {test_user_token}"}
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    start_time = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0)
    end_time = start_time - timedelta(minutes=30)
    payload = {
        "doctor_id": test_doctor.id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        resp = await ac.post(
            "/api/v1/appointments", json=payload, headers=headers
        )
        assert resp.status_code == 400
