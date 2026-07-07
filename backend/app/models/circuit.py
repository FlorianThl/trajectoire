import uuid
from datetime import datetime

from geoalchemy2 import Geography
from sqlalchemy import ARRAY, Boolean, CheckConstraint, DateTime, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Circuit(Base):
    __tablename__ = "circuits"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    address: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(String(100))
    postal_code: Mapped[str | None] = mapped_column(String(10))
    country: Mapped[str | None] = mapped_column(String(100), default="France")
    location: Mapped[str] = mapped_column(Geography(geometry_type="POINT", srid=4326), nullable=False)
    length_km: Mapped[float | None] = mapped_column(Numeric(6, 3))
    layout_type: Mapped[str | None] = mapped_column(String(50), default="permanent")
    runoff_areas: Mapped[str | None] = mapped_column(String(50), default="asphalte")
    has_electricity: Mapped[bool] = mapped_column(default=False)
    has_compressor: Mapped[bool] = mapped_column(default=False)
    has_fuel_station: Mapped[bool] = mapped_column(default=False)
    noise_limit_db: Mapped[float | None] = mapped_column(Numeric(5, 1))
    has_noise_restriction: Mapped[bool] = mapped_column(default=False)
    allowed_categories: Mapped[list | None] = mapped_column(ARRAY(String(20)), default=["auto"])
    image_url: Mapped[str | None] = mapped_column(Text)
    website_url: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    events = relationship("Event", back_populates="circuit", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("noise_limit_db >= 80 AND noise_limit_db <= 130", name="ck_circuit_noise"),
    )
