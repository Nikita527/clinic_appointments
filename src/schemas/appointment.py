from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppointmentCreate(BaseModel):
    """Данные для создания записи к врачу."""

    doctor_id: int
    start_time: datetime
    end_time: datetime


class AppointmentRead(BaseModel):
    """Данные для чтения записи к врачу."""

    id: int
    user_id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime

    model_config = ConfigDict(from_attributes=True)
