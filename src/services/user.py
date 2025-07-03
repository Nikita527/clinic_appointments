from typing import Optional

from passlib.context import CryptContext

from src.models.users import User as UserModel
from src.repositories.users import User
from src.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Сервис для работы с пользователями."""

    def __init__(self, repo: User):
        """Инициализация сервиса."""
        self.repo = repo

    async def authenticate_user(
        self, email: str, password: str
    ) -> Optional[UserModel]:
        """Проверяет логин и пароль пользователя."""
        user = await self.repo.get_by_email(email)
        if not user:
            return None
        if not pwd_context.verify(password, str(user.hashed_password)):
            return None
        return user

    async def create_user(self, user_in: UserCreate):
        """Создание пользователя."""
        hashed_password = pwd_context.hash(user_in.password)
        return await self.repo.create(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            email=user_in.email,
            hashed_password=hashed_password,
        )
