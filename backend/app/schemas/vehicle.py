import uuid

from pydantic import BaseModel, ConfigDict, field_validator


NOISE_MIN = 80
NOISE_MAX = 130


class VehicleCreate(BaseModel):
    vehicle_type: str
    brand: str
    model: str
    year: int
    tires: str | None = "road"
    brakes: str | None = "stock"
    noise_level_db: float | None = None

    @field_validator("noise_level_db")
    @classmethod
    def validate_noise(cls, v: float | None) -> float | None:
        if v is not None and (v < NOISE_MIN or v > NOISE_MAX):
            raise ValueError(f"Le niveau sonore doit être entre {NOISE_MIN} et {NOISE_MAX} dB")
        return v


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

    @field_validator("noise_level_db")
    @classmethod
    def validate_noise(cls, v: float | None) -> float | None:
        if v is not None and (v < NOISE_MIN or v > NOISE_MAX):
            raise ValueError(f"Le niveau sonore doit être entre {NOISE_MIN} et {NOISE_MAX} dB")
        return v
