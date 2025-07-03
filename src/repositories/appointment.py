from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.appoitment import Appointment as AppointmentModel
from src.schemas.appointment import AppointmentCreate


class Appointment:
    """Репозиторий для работы с записями к врачу."""

    def __init__(self, session: AsyncSession):
        """Инициализация репозитория."""
        self.session = session

    async def get_by_id(
        self, appointment_id: int
    ) -> Optional[AppointmentModel]:
        """Получение записи к врачу."""
        return await self.session.get(AppointmentModel, appointment_id)

    async def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> Sequence[AppointmentModel]:
        """Получение всех записей к врачу."""
        result = await self.session.execute(
            select(AppointmentModel).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_overlapping_appointments(
        self,
        doctor_id: int,
        start_time: datetime,
        end_time: datetime,
    ) -> Optional[AppointmentModel]:
        """Получение пересекающихся записей к врачу."""
        result = await self.session.execute(
            select(AppointmentModel).where(
                AppointmentModel.doctor_id == doctor_id,
                AppointmentModel.start_time < end_time,
                AppointmentModel.end_time > start_time,
            )
        )
        return result.scalars().first()

    async def create(
        self, user_id: int, appointment_in: AppointmentCreate
    ) -> AppointmentModel:
        """Создание записи к врачу."""
        appointment = AppointmentModel(
            user_id=user_id,
            doctor_id=appointment_in.doctor_id,
            start_time=appointment_in.start_time,
            end_time=appointment_in.end_time,
        )
        self.session.add(appointment)
        try:
            await self.session.commit()
            await self.session.refresh(appointment)
        except IntegrityError:
            await self.session.rollback()
            raise
        return appointment

    async def delete(self, appointment_id: int) -> None:
        """Удаление записи к врачу."""
        appointment = await self.get_by_id(appointment_id)
        if appointment:
            await self.session.delete(appointment)
            await self.session.commit()
