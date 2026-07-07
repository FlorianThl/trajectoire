import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: str | None = None
    category: str = "auto"
    license_type: str = "none"
    license_number: str | None = None
    license_expiry: date | None = None
    address: str | None = None
    city: str | None = None
    postal_code: str | None = None
    country: str | None = "France"
    level: str = "debutant"


class UserRead(BaseModel):
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    phone: str | None
    category: str
    license_type: str
    license_number: str | None
    license_expiry: date | None
    address: str | None
    city: str | None
    postal_code: str | None
    country: str | None
    level: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    category: str | None = None
    license_type: str | None = None
    license_number: str | None = None
    license_expiry: date | None = None
    address: str | None = None
    city: str | None = None
    postal_code: str | None = None
    country: str | None = None
    level: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
