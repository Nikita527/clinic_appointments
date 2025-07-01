from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.users import User as UserModel


class User:
    """Репозиторий пользователей."""

    def __init__(self, session: AsyncSession):
        """Инициализация репозитория."""
        self.session = session

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        """Получение пользователя по email."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalars().first()

    async def create(
        self, first_name, last_name, email, hashed_password
    ) -> UserModel:
        """Создание пользователя."""
        user = UserModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            hashed_password=hashed_password,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
