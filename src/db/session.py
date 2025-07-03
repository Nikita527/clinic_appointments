from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine: AsyncEngine = create_async_engine(settings.database_url, echo=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)  # type: ignore


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии для работы с базой данных."""
    async with async_session() as session:
        yield session
