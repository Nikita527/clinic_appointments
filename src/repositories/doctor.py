from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.doctor import Doctor as DoctorModel
from src.schemas.doctor import DoctorRead


class Doctor:
    """Репозиторий для работы с врачами."""

    def __init__(self, session: AsyncSession):
        """Инициализация репозитория."""
        self.session = session

    async def get_all(self) -> Sequence[DoctorModel]:
        """Получение всех врачей."""
        result = await self.session.execute(select(DoctorModel))
        return result.scalars().all()

    async def get_by_id(self, doctor_id: int) -> Optional[DoctorModel]:
        """Получение врача по id."""
        result = await self.session.execute(
            select(DoctorModel).where(DoctorModel.id == doctor_id)
        )
        return result.scalars().first()

    async def create(self, doctor_in: DoctorRead) -> DoctorModel:
        """Создание врача."""
        doctor = DoctorModel(
            first_name=doctor_in.first_name,
            last_name=doctor_in.last_name,
            specialization=doctor_in.specialization,
        )
        self.session.add(doctor)
        await self.session.commit()
        await self.session.refresh(doctor)
        return doctor
