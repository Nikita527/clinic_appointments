from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import (
    create_access_token,
    create_refresh_token,
    get_current_user,
)
from src.core.config import settings
from src.db.session import get_session
from src.repositories.users import User
from src.schemas.auth import TokenPair, TokenRefresh
from src.schemas.user import UserCreate, UserRead
from src.services.user import UserService

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post(
    "/register",
    response_model=UserRead,
    summary="Регистрация нового пользователя",
)
async def register(
    user_in: UserCreate, session: AsyncSession = Depends(get_session)
):
    """Регистрация нового пользователя."""
    user_repo = User(session)
    user_service = UserService(user_repo)
    return await user_service.create_user(user_in)


@router.post("/login", response_model=TokenPair, summary="Авторизация")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    """Аутентификация пользователя."""
    user_repo = User(session)
    user_service = UserService(user_repo)
    user = await user_service.authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный логин или пароль",
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", summary="Обновление access token")
async def refresh_token(
    data: TokenRefresh, session: AsyncSession = Depends(get_session)
):
    """
    Получение нового access token.

    Принимает refresh token, проверяет его и возвращает новый access token.
    """
    try:
        payload = jwt.decode(
            data.refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token: missing subject",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Опционально: проверить, существует ли пользователь в базе данных,
    # чтобы убедиться,
    # что токен действительно принадлежит валидному пользователю.
    user_repo = User(session)
    user = await user_repo.get_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаем новый access token
    new_access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes
    )
    new_access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=new_access_token_expires
    )

    return {"access_token": new_access_token, "token_type": "bearer"}


@router.get(
    "/me", response_model=UserRead, summary="Данные текущего пользователя"
)
async def read_current_user(
    current_user: UserRead = Depends(get_current_user),
):
    """Возвращает данные текущего аутентифицированного пользователя."""
    return current_user
