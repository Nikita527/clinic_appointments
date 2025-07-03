from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.schemas.appointment import AppointmentCreate
from src.services.appointment import AppointmentService


@pytest.mark.asyncio
async def test_create_appointment_success() -> None:
    """Проверка создания записи к врачу."""
    repo_mock = MagicMock()
    repo_mock.get_overlapping_appointments = AsyncMock(return_value=None)
    repo_mock.create = AsyncMock(return_value="appointment_obj")
    service = AppointmentService(repo_mock)
    now = datetime.now(timezone.utc)
    appointment_in = AppointmentCreate(
        doctor_id=1,
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=1, minutes=30),
    )

    result = await service.create_appointment(
        user_id=1, appointment_in=appointment_in
    )

    assert result == "appointment_obj"
    repo_mock.get_overlapping_appointments.assert_awaited_once()
    repo_mock.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_appointment_overlap() -> None:
    """Проверка создания записи к врачу при пересечении."""
    repo_mock = MagicMock()
    repo_mock.get_overlapping_appointments = AsyncMock(return_value="exists")
    service = AppointmentService(repo_mock)
    start_time = datetime.now(timezone.utc) + timedelta(days=1)
    end_time = start_time + timedelta(minutes=30)
    appointment_in = AppointmentCreate(
        doctor_id=1, start_time=start_time, end_time=end_time
    )

    with pytest.raises(ValueError):
        await service.create_appointment(
            user_id=1, appointment_in=appointment_in
        )
