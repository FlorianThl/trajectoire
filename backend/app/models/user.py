import uuid
from datetime import date, datetime

from geoalchemy2 import Geography
from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, Enum, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20))
    category: Mapped[str] = mapped_column(Enum("auto", "moto", "both", name="pilot_category"), default="auto")
    license_type: Mapped[str] = mapped_column(Enum("ffsa", "ffm", "none", name="license_type"), default="none")
    license_number: Mapped[str | None] = mapped_column(String(50))
    license_expiry: Mapped[date | None] = mapped_column(Date)
    address: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(String(100))
    postal_code: Mapped[str | None] = mapped_column(String(10))
    country: Mapped[str | None] = mapped_column(String(100), default="France")
    location: Mapped[str | None] = mapped_column(Geography(geometry_type="POINT", srid=4326))
    level: Mapped[str] = mapped_column(
        String(20), default="debutant"
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    vehicles = relationship("Vehicle", back_populates="user", cascade="all, delete-orphan")
    lap_records = relationship("LapRecord", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("level IN ('debutant', 'intermediaire', 'confirme')", name="ck_user_level"),
    )
