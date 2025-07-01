from sqlalchemy import Column, Integer, String

from .base import Base


class Doctor(Base):
    """Модель врача."""

    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    specialization = Column(String(128), nullable=True)
