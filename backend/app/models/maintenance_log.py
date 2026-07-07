import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, Numeric, FetchedValue
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    consumable: Mapped[str] = mapped_column(
        Enum("plaquettes", "disques", "huile", "liquide_frein", "pneus", name="consumable_type"),
        nullable=False,
    )
    max_laps: Mapped[int] = mapped_column(Integer, nullable=False)
    current_laps: Mapped[int] = mapped_column(Integer, default=0)
    wear_percent: Mapped[float | None] = mapped_column(Numeric(5, 2), FetchedValue())
    last_replaced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    alert_threshold: Mapped[float] = mapped_column(Float, default=80.0)
    is_alerted: Mapped[bool | None] = mapped_column(Boolean, FetchedValue())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)

    vehicle = relationship("Vehicle", back_populates="maintenance_logs")
