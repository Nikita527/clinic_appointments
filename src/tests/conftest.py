import os
from uuid import uuid4

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import Base
from src.repositories.doctor import Doctor
from src.repositories.users import User
from src.schemas.doctor import DoctorCreate
from src.schemas.user import UserCreate
from src.services.user import UserService

POSTGRES_HOST = os.getenv("POSTGRES_HOST_FOR_TESTS", "localhost")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


@pytest_asyncio.fixture
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture
async def async_engine():
    engine = create_async_engine(DATABASE_URL, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def async_session(async_engine):
    async_session = sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def test_user_token(async_session):
    user_repo = User(async_session)
    user_service = UserService(user_repo)
    user_in = UserCreate(
        first_name="Test",
        last_name="User",
        email=f"testuser_{uuid4()}@example.com",
        password="testpassword",
    )
    await user_service.create_user(user_in)
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        # Получить токен
        resp = await ac.post(
            "/api/v1/auth/login",
            data={
                "username": user_in.email,
                "password": user_in.password,
            },
        )
        assert resp.status_code == 200
        return resp.json()["access_token"]


@pytest_asyncio.fixture
async def test_doctor(async_session):
    doctor_repo = Doctor(async_session)
    doctor_in = DoctorCreate(
        first_name="Doc", last_name=f"Test{uuid4()}", specialization="Терапевт"
    )
    doctor = await doctor_repo.create(doctor_in)
    return doctor
