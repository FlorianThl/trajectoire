import uuid
from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Enum, Integer, Numeric, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vehicle_type: Mapped[str] = mapped_column(Enum("auto", "moto", name="vehicle_type"), nullable=False)
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    tires: Mapped[str | None] = mapped_column(Enum("slicks", "semi_slicks", "road", name="tire_type"), default="road")
    brakes: Mapped[str | None] = mapped_column(Enum("stock", "sport", "racing", name="brake_type"), default="stock")
    noise_level_db: Mapped[float | None] = mapped_column(Numeric(5, 1))
    total_laps: Mapped[int] = mapped_column(Integer, default=0)
    total_track_km: Mapped[float] = mapped_column(Numeric(10, 1), default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="vehicles")
    lap_records = relationship("LapRecord", back_populates="vehicle")
    maintenance_logs = relationship("MaintenanceLog", back_populates="vehicle", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("year >= 1980 AND year <= 2030", name="ck_vehicle_year"),
        CheckConstraint("noise_level_db >= 80 AND noise_level_db <= 130", name="ck_vehicle_noise"),
    )
