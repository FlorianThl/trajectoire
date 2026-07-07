import uuid

from pydantic import BaseModel, ConfigDict


class VehicleCreate(BaseModel):
    vehicle_type: str
    brand: str
    model: str
    year: int
    tires: str | None = "road"
    brakes: str | None = "stock"
    noise_level_db: float | None = None


class VehicleRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    vehicle_type: str
    brand: str
    model: str
    year: int
    tires: str | None
    brakes: str | None
    noise_level_db: float | None
    total_laps: int
    total_track_km: float | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class VehicleUpdate(BaseModel):
    vehicle_type: str | None = None
    brand: str | None = None
    model: str | None = None
    year: int | None = None
    tires: str | None = None
    brakes: str | None = None
    noise_level_db: float | None = None
