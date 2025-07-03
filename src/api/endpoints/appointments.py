from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import get_current_user
from src.db.session import get_session
from src.models.appoitment import Appointment
from src.repositories.appointment import Appointment as AppointmentRepo
from src.schemas.appointment import AppointmentCreate, AppointmentRead
from src.schemas.user import UserRead
from src.services.appointment import AppointmentService

router = APIRouter(prefix="/appointments", tags=["Запись на прием к врачу"])


def get_appointment_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AppointmentService:
    """Получение сервиса для работы с записями к врачу."""
    repo = AppointmentRepo(session)
    return AppointmentService(repo)


@router.post(
    "",
    response_model=AppointmentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создание записи к врачу",
)
async def create_appointment(
    appointment_in: AppointmentCreate,
    current_user: UserRead = Depends(get_current_user),
    service: AppointmentService = Depends(get_appointment_service),
) -> Appointment:
    """Создание записи к врачу."""
    try:
        appointment = await service.create_appointment(
            current_user.id, appointment_in
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="На выбранное время уже есть запись к этому врачу.",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return appointment


@router.get(
    "/{appointment_id}",
    response_model=AppointmentRead,
    summary="Получение записи к врачу по идентификатору",
    description="Можно получить только свои записи.",
)
async def get_appointment(
    appointment_id: int,
    current_user: UserRead = Depends(get_current_user),
    service: AppointmentService = Depends(get_appointment_service),
) -> Appointment:
    """Получение записи к врачу."""
    appointment = await service.get_appointment(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Запись не найдена.")
    if appointment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к записи.")
    return appointment
