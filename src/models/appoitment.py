from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class Appointment(Base):
    """Модель записи к врачу."""

    __tablename__ = "appointments"
    __table_args__ = (
        UniqueConstraint("doctor_id", "start_time", name="uq_doctor_time"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    doctor_id = Column(
        Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False
    )
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User")
    doctor = relationship("Doctor")
