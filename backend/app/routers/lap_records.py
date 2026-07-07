import csv
import io
import uuid
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.circuit import Circuit
from app.models.lap_record import LapRecord
from app.schemas.lap import LapRecordCreate, LapRecordRead

router = APIRouter(prefix="/laps", tags=["laps"])


@router.get("", response_model=list[LapRecordRead])
async def list_laps(
    circuit_id: uuid.UUID | None = None,
    vehicle_id: uuid.UUID | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    query = select(LapRecord).where(LapRecord.user_id == current_user.id)
    if circuit_id is not None:
        query = query.where(LapRecord.circuit_id == circuit_id)
    if vehicle_id is not None:
        query = query.where(LapRecord.vehicle_id == vehicle_id)
    query = query.order_by(LapRecord.created_at.desc())
    result = await db.execute(query)
    laps = result.scalars().all()
    return [
        LapRecordRead(
            id=l.id, user_id=l.user_id, vehicle_id=l.vehicle_id,
            circuit_id=l.circuit_id, event_id=l.event_id,
            lap_time=str(l.lap_time), lap_number=l.lap_number,
            total_laps_session=l.total_laps_session, notes=l.notes,
            validated_at=l.validated_at, created_at=l.created_at,
        )
        for l in laps
    ]


@router.post("", response_model=LapRecordRead, status_code=status.HTTP_201_CREATED)
async def create_lap(
    data: LapRecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    circuit_q = await db.execute(
        select(Circuit).where(Circuit.id == data.circuit_id, Circuit.is_active == True)
    )
    circuit = circuit_q.scalar_one_or_none()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")

    if data.vehicle_id is not None:
        vehicle_q = await db.execute(
            select(Vehicle).where(Vehicle.id == data.vehicle_id, Vehicle.user_id == current_user.id)
        )
        vehicle = vehicle_q.scalar_one_or_none()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")

        if data.total_laps_session:
            vehicle.total_laps = (vehicle.total_laps or 0) + data.total_laps_session
            current_km = float(vehicle.total_track_km) if vehicle.total_track_km else 0
            if circuit.length_km:
                vehicle.total_track_km = current_km + (data.total_laps_session * float(circuit.length_km))

    parts = data.lap_time.replace(",", ".").split(":")
    try:
        if len(parts) == 3:
            td = timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=float(parts[2]))
        elif len(parts) == 2:
            td = timedelta(minutes=int(parts[0]), seconds=float(parts[1]))
        else:
            td = timedelta(seconds=float(parts[0]))
    except (ValueError, IndexError):
        raise HTTPException(status_code=422, detail="Invalid lap_time format. Use M:SS.mmm or H:M:SS.mmm")

    lap = LapRecord(
        user_id=current_user.id,
        vehicle_id=data.vehicle_id,
        circuit_id=data.circuit_id,
        event_id=data.event_id,
        lap_time=td,
        lap_number=data.lap_number,
        total_laps_session=data.total_laps_session,
        notes=data.notes,
    )
    db.add(lap)
    await db.commit()
    await db.refresh(lap)

    lap_read = LapRecordRead(
        id=lap.id,
        user_id=lap.user_id,
        vehicle_id=lap.vehicle_id,
        circuit_id=lap.circuit_id,
        event_id=lap.event_id,
        lap_time=str(lap.lap_time),
        lap_number=lap.lap_number,
        total_laps_session=lap.total_laps_session,
        notes=lap.notes,
        validated_at=lap.validated_at,
        created_at=lap.created_at,
    )
    return lap_read


@router.get("/stats/progression")
async def lap_progression_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = await db.execute(
        select(LapRecord).where(LapRecord.user_id == current_user.id)
        .options(joinedload(LapRecord.circuit))
        .order_by(LapRecord.created_at.asc())
    )
    laps = result.scalars().all()

    circuits_cache: dict[str, str] = {}
    groups: dict[str, dict] = {}
    for l in laps:
        cid = str(l.circuit_id)
        if cid not in circuits_cache:
            circuits_cache[cid] = l.circuit.name if l.circuit else cid[:8]
        if cid not in groups:
            groups[cid] = {"circuit_id": cid, "circuit_name": circuits_cache[cid], "laps": []}
        sec = l.lap_time.total_seconds()
        groups[cid]["laps"].append({
            "date": l.created_at.strftime("%Y-%m-%d"),
            "lap_time": str(l.lap_time),
            "seconds": round(sec, 3),
        })

    result_list = []
    for cid, g in groups.items():
        best = min(g["laps"], key=lambda x: x["seconds"])
        result_list.append({
            "circuit_id": cid,
            "circuit_name": g["circuit_name"],
            "laps": g["laps"],
            "best_lap": best["lap_time"],
            "best_seconds": best["seconds"],
            "total_laps": len(g["laps"]),
        })
    return result_list


@router.get("/export/csv")
async def export_laps_csv(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = await db.execute(
        select(LapRecord).where(LapRecord.user_id == current_user.id)
        .options(joinedload(LapRecord.circuit), joinedload(LapRecord.vehicle))
        .order_by(LapRecord.created_at.desc())
    )
    laps = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["circuit", "date", "temps", "vehicule", "tours_session", "notes"])
    for l in laps:
        circuit_name = l.circuit.name if l.circuit else str(l.circuit_id)[:8]
        vehicle_name = f"{l.vehicle.brand} {l.vehicle.model}" if l.vehicle else ""
        writer.writerow([
            circuit_name,
            l.created_at.strftime("%Y-%m-%d"),
            str(l.lap_time),
            vehicle_name,
            l.total_laps_session or "",
            l.notes or "",
        ])

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=chronos.csv"},
    )


@router.get("/stats/vehicle")
async def lap_vehicle_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    vehicles_q = await db.execute(
        select(Vehicle).where(Vehicle.user_id == current_user.id)
    )
    vehicles = vehicles_q.scalars().all()

    result_list = []
    for v in vehicles:
        count_q = await db.execute(
            select(func.count(LapRecord.id)).where(
                LapRecord.vehicle_id == v.id,
                LapRecord.user_id == current_user.id,
            )
        )
        lap_count = count_q.scalar() or 0
        result_list.append({
            "id": str(v.id),
            "brand": v.brand,
            "model": v.model,
            "total_laps": v.total_laps,
            "total_track_km": float(v.total_track_km) if v.total_track_km else 0,
            "lap_records_count": lap_count,
        })
    return result_list


@router.delete("/{lap_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lap(
    lap_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    result = await db.execute(
        select(LapRecord).where(
            LapRecord.id == lap_id,
            LapRecord.user_id == current_user.id,
        )
    )
    lap = result.scalar_one_or_none()
    if not lap:
        raise HTTPException(status_code=404, detail="Lap not found")
    await db.delete(lap)
    await db.commit()
