import uuid
from datetime import datetime, timedelta

from sqlalchemy import DateTime, ForeignKey, Integer, Interval, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class LapRecord(Base):
    __tablename__ = "lap_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vehicle_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("vehicles.id", ondelete="SET NULL"))
    circuit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("circuits.id", ondelete="CASCADE"), nullable=False)
    event_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("events.id", ondelete="SET NULL"))
    lap_time: Mapped[timedelta] = mapped_column(Interval, nullable=False)
    lap_number: Mapped[int | None] = mapped_column(Integer)
    total_laps_session: Mapped[int | None] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(Text)
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=datetime.now)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="lap_records")
    vehicle = relationship("Vehicle", back_populates="lap_records")
    circuit = relationship("Circuit")
