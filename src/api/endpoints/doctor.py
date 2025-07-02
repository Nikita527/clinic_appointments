from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import get_current_user
from src.db.session import get_session
from src.repositories.doctor import Doctor
from src.schemas.doctor import DoctorCreate, DoctorRead

router = APIRouter(prefix="/doctors", tags=["Врачи"])


@router.post(
    "/create",
    response_model=DoctorRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_doctor(
    doctor_in: DoctorCreate,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Создание врача."""
    doctor_repo = Doctor(session)
    return await doctor_repo.create(doctor_in)
