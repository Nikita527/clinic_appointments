from sqlalchemy import Column, Integer, String

from .base import Base


class User(Base):
    """Модель пользователя."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(128), unique=True, nullable=False)
    hashed_password = Column(String)
