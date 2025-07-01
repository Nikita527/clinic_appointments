from pydantic import BaseModel, EmailStr


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

    class Config:
        from_attributes = True
