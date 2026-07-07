import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class CircuitRead(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    description: str | None
    address: str | None
    city: str | None
    postal_code: str | None
    country: str | None
    length_km: float | None
    layout_type: str | None
    runoff_areas: str | None
    has_electricity: bool
    has_compressor: bool
    has_fuel_station: bool
    noise_limit_db: float | None
    has_noise_restriction: bool
    allowed_categories: list[str] | None
    image_url: str | None
    website_url: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CircuitSearchResult(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    city: str | None
    length_km: float | None
    noise_limit_db: float | None
    has_noise_restriction: bool
    allowed_categories: list[str] | None
    image_url: str | None
    distance_km: float | None
    events_count: int
    lat: float | None = None
    lon: float | None = None


class CircuitSearchParams(BaseModel):
    lat: float | None = None
    lon: float | None = None
    radius_km: float | None = None
    vehicle_noise_db: float | None = None
    vehicle_category: str | None = None
    min_date: date | None = None
    max_date: date | None = None
    level: str | None = None

