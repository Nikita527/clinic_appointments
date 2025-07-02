from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """Схема создания пользователя."""

    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    """Схема чтения пользователя."""

    id: int
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
