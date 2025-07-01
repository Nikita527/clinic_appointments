from pydantic import BaseModel


class Token(BaseModel):
    """Схема токена."""

    access_token: str
    token_type: str


class TokenRefresh(BaseModel):
    """Схема обновления токена."""

    refresh_token: str


class TokenPair(BaseModel):
    """Схема ответа при логине."""

    access_token: str
    refresh_token: str
    token_type: str
