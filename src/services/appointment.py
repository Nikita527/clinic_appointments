from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.exc import IntegrityError

from src.models.appoitment import Appointment
from src.repositories.appointment import Appointment as AppointmentRepo
from src.schemas.appointment import AppointmentCreate


class AppointmentService:
    def __init__(self, repo: AppointmentRepo) -> None:
        """Инициализация сервиса."""
        self.repo = repo

    async def create_appointment(
        self, user_id: int, appointment_in: AppointmentCreate
    ) -> Appointment:
        """Создание записи к врачу(бизнес логика)."""
        now = datetime.now(timezone.utc)
        if appointment_in.start_time < now:
            raise ValueError(
                "Нельзя записаться в прошлое или на текущее время"
            )
        if appointment_in.end_time < appointment_in.start_time:
            raise ValueError(
                "Время окончания должно быть позже времени начала"
            )
        overlapping = await self.repo.get_overlapping_appointments(
            doctor_id=appointment_in.doctor_id,
            start_time=appointment_in.start_time,
            end_time=appointment_in.end_time,
        )
        if overlapping:
            raise ValueError(
                "На выбранное время уже есть запись к этому врачу."
            )
        try:
            return await self.repo.create(user_id, appointment_in)
        except IntegrityError:
            # Можно логировать, отправлять метрики и т.д.
            raise

    async def get_appointment(
        self, appointment_id: int
    ) -> Optional[Appointment]:
        """Получение записи к врачу(бизнес логика)."""
        return await self.repo.get_by_id(appointment_id)
