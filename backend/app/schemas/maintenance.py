import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MaintenanceLogCreate(BaseModel):
    consumable: str
    max_laps: int
    alert_threshold: float = 80.0


class MaintenanceLogRead(BaseModel):
    id: uuid.UUID
    vehicle_id: uuid.UUID
    consumable: str
    max_laps: int
    current_laps: int
    wear_percent: float | None
    last_replaced_at: datetime | None
    alert_threshold: float
    is_alerted: bool | None

    model_config = ConfigDict(from_attributes=True)


class MaintenanceLogUpdate(BaseModel):
    current_laps: int | None = None
    last_replaced_at: datetime | None = None
    alert_threshold: float | None = None


class LapRecordCreate(BaseModel):
    vehicle_id: uuid.UUID | None = None
    circuit_id: uuid.UUID
    event_id: uuid.UUID | None = None
    lap_time: str
    lap_number: int | None = None
    total_laps_session: int | None = None
    notes: str | None = None


class LapRecordRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    vehicle_id: uuid.UUID | None
    circuit_id: uuid.UUID
    event_id: uuid.UUID | None
    lap_time: str
    lap_number: int | None
    total_laps_session: int | None
    notes: str | None
    validated_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
