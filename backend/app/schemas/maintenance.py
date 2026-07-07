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
