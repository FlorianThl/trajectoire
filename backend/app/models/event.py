import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    circuit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("circuits.id", ondelete="CASCADE"), nullable=False)
    organizer_name: Mapped[str] = mapped_column(String(200), nullable=False)
    organizer_url: Mapped[str | None] = mapped_column(Text)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    has_debutant: Mapped[bool] = mapped_column(Boolean, default=False)
    has_intermediaire: Mapped[bool] = mapped_column(Boolean, default=False)
    has_confirme: Mapped[bool] = mapped_column(Boolean, default=False)
    price_base: Mapped[float | None] = mapped_column(Numeric(8, 2))
    price_license: Mapped[float | None] = mapped_column(Numeric(8, 2))
    booking_url: Mapped[str | None] = mapped_column(Text)
    spots_available: Mapped[int | None] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    scraped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    circuit = relationship("Circuit", back_populates="events")

    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="ck_event_dates"),
    )
