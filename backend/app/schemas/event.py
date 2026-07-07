import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class EventRead(BaseModel):
    id: uuid.UUID
    circuit_id: uuid.UUID
    circuit_name: str | None = None
    organizer_name: str
    organizer_url: str | None
    start_date: date
    end_date: date
    has_debutant: bool
    has_intermediaire: bool
    has_confirme: bool
    price_base: float | None
    price_license: float | None
    booking_url: str | None
    spots_available: int | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
