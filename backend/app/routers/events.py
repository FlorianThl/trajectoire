import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models.circuit import Circuit
from app.models.event import Event
from app.schemas.event import EventRead

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventRead])
async def list_events(
    circuit_id: uuid.UUID | None = Query(None),
    min_date: date | None = Query(None),
    max_date: date | None = Query(None),
    level: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Event).where(Event.is_active == True)

    if circuit_id is not None:
        query = query.where(Event.circuit_id == circuit_id)
    if min_date is not None:
        query = query.where(Event.start_date >= min_date)
    if max_date is not None:
        query = query.where(Event.end_date <= max_date)
    if level == "debutant":
        query = query.where(Event.has_debutant == True)
    elif level == "intermediaire":
        query = query.where(Event.has_intermediaire == True)
    elif level == "confirme":
        query = query.where(Event.has_confirme == True)

    query = query.order_by(Event.start_date.asc())
    result = await db.execute(query)
    events = result.scalars().all()

    circuit_ids = {e.circuit_id for e in events}
    circuits_q = await db.execute(
        select(Circuit).where(Circuit.id.in_(circuit_ids))
    )
    circuits = {c.id: c.name for c in circuits_q.scalars().all()}

    return [
        EventRead(
            id=e.id,
            circuit_id=e.circuit_id,
            circuit_name=circuits.get(e.circuit_id),
            organizer_name=e.organizer_name,
            organizer_url=e.organizer_url,
            start_date=e.start_date,
            end_date=e.end_date,
            has_debutant=e.has_debutant,
            has_intermediaire=e.has_intermediaire,
            has_confirme=e.has_confirme,
            price_base=float(e.price_base) if e.price_base else None,
            price_license=float(e.price_license) if e.price_license else None,
            booking_url=e.booking_url,
            spots_available=e.spots_available,
            is_active=e.is_active,
            created_at=e.created_at,
        )
        for e in events
    ]
