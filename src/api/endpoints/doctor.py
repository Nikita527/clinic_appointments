from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import get_current_user
from src.db.session import get_session
from src.models.doctor import Doctor
from src.repositories.doctor import Doctor as DoctorRepo
from src.schemas.doctor import DoctorCreate, DoctorRead
from src.schemas.user import UserRead

router = APIRouter(prefix="/doctors", tags=["Врачи"])


@router.post(
    "/create",
    response_model=DoctorRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_doctor(
    doctor_in: DoctorCreate,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Doctor:
    """Создание врача."""
    doctor_repo = DoctorRepo(session)
    return await doctor_repo.create(doctor_in)
