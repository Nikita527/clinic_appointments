from pydantic import BaseModel


class DoctorCreate(BaseModel):
    """Схема создания врача."""

    first_name: str
    last_name: str
    specialization: str | None = None


class DoctorRead(BaseModel):
    """Схема чтения врача."""

    id: int
    first_name: str
    last_name: str
    specialization: str | None = None

    class Config:
        from_attributes = True
