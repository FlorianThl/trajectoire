import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from geoalchemy2.functions import ST_Distance, ST_MakePoint, ST_SetSRID, ST_X, ST_Y
from sqlalchemy import func, select, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.models.circuit import Circuit
from app.models.event import Event
from app.schemas.circuit import CircuitRead, CircuitSearchResult
from app.schemas.event import EventRead

router = APIRouter(prefix="/circuits", tags=["circuits"])


@router.get("", response_model=list[CircuitSearchResult])
async def search_circuits(
    lat: float | None = Query(None),
    lon: float | None = Query(None),
    radius_km: float | None = Query(None),
    vehicle_noise_db: float | None = Query(None),
    vehicle_category: str | None = Query(None),
    min_date: date | None = Query(None),
    max_date: date | None = Query(None),
    level: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Circuit).where(Circuit.is_active == True)

    if vehicle_noise_db is not None:
        query = query.where(
            case(
                (Circuit.has_noise_restriction == True, Circuit.noise_limit_db >= vehicle_noise_db),
                else_=True,
            )
        )

    if vehicle_category is not None:
        query = query.where(Circuit.allowed_categories.any(vehicle_category))

    if level == "debutant":
        query = query.where(
            Event.has_debutant == True
        ).join(Event, Circuit.id == Event.circuit_id)
    elif level == "intermediaire":
        query = query.where(
            Event.has_intermediaire == True
        ).join(Event, Circuit.id == Event.circuit_id)
    elif level == "confirme":
        query = query.where(
            Event.has_confirme == True
        ).join(Event, Circuit.id == Event.circuit_id)

    if min_date is not None:
        query = query.join(Event, Circuit.id == Event.circuit_id).where(Event.start_date >= min_date)
    if max_date is not None:
        query = query.join(Event, Circuit.id == Event.circuit_id).where(Event.end_date <= max_date)

    query = query.distinct()

    result = await db.execute(query)
    circuits = result.scalars().all()

    results = []
    for c in circuits:
        distance_km = None
        if lat is not None and lon is not None:
            user_point = ST_SetSRID(ST_MakePoint(lon, lat), 4326)
            distance = await db.execute(
                select(ST_Distance(c.location, user_point))
            )
            d = distance.scalar()
            distance_km = round(float(d) / 1000, 1) if d else None

        events_count_q = await db.execute(
            select(func.count(Event.id)).where(
                Event.circuit_id == c.id,
                Event.is_active == True,
            )
        )
        events_count = events_count_q.scalar() or 0

        circuit_lat = await db.scalar(select(ST_Y(c.location))) if c.location else None
        circuit_lon = await db.scalar(select(ST_X(c.location))) if c.location else None

        results.append(CircuitSearchResult(
            id=c.id,
            name=c.name,
            slug=c.slug,
            city=c.city,
            length_km=float(c.length_km) if c.length_km else None,
            noise_limit_db=float(c.noise_limit_db) if c.noise_limit_db else None,
            has_noise_restriction=c.has_noise_restriction,
            allowed_categories=c.allowed_categories,
            image_url=c.image_url,
            distance_km=distance_km,
            events_count=events_count,
            lat=float(circuit_lat) if circuit_lat else None,
            lon=float(circuit_lon) if circuit_lon else None,
        ))

    if radius_km is not None:
        results = [r for r in results if r.distance_km is None or r.distance_km <= radius_km]

    return results


@router.get("/{circuit_id}", response_model=CircuitRead)
async def get_circuit(
    circuit_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Circuit).where(Circuit.id == circuit_id, Circuit.is_active == True)
    )
    circuit = result.scalar_one_or_none()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit


@router.get("/{circuit_id}/events", response_model=list[EventRead])
async def get_circuit_events(
    circuit_id: uuid.UUID,
    min_date: date | None = Query(None),
    max_date: date | None = Query(None),
    level: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    circuit_q = await db.execute(
        select(Circuit).where(Circuit.id == circuit_id, Circuit.is_active == True)
    )
    circuit = circuit_q.scalar_one_or_none()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")

    query = select(Event).where(
        Event.circuit_id == circuit_id,
        Event.is_active == True,
    )

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

    return [
        EventRead(
            id=e.id,
            circuit_id=e.circuit_id,
            circuit_name=circuit.name,
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
