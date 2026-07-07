import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.maintenance_log import MaintenanceLog
from app.schemas.maintenance import MaintenanceLogCreate, MaintenanceLogRead, MaintenanceLogUpdate

router = APIRouter(prefix="/vehicles/{vehicle_id}/maintenance", tags=["maintenance"])


async def _get_vehicle(vehicle_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession) -> Vehicle:
    result = await db.execute(
        select(Vehicle).where(Vehicle.id == vehicle_id, Vehicle.user_id == user_id)
    )
    vehicle = result.scalar_one_or_none()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.get("", response_model=list[MaintenanceLogRead])
async def list_maintenance(
    vehicle_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    await _get_vehicle(vehicle_id, current_user.id, db)
    result = await db.execute(
        select(MaintenanceLog).where(MaintenanceLog.vehicle_id == vehicle_id)
    )
    return result.scalars().all()


@router.post("", response_model=MaintenanceLogRead, status_code=status.HTTP_201_CREATED)
async def create_maintenance_log(
    vehicle_id: uuid.UUID,
    data: MaintenanceLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    await _get_vehicle(vehicle_id, current_user.id, db)
    log = MaintenanceLog(vehicle_id=vehicle_id, **data.model_dump())
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@router.patch("/{log_id}", response_model=MaintenanceLogRead)
async def update_maintenance_log(
    vehicle_id: uuid.UUID,
    log_id: uuid.UUID,
    data: MaintenanceLogUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    await _get_vehicle(vehicle_id, current_user.id, db)
    result = await db.execute(
        select(MaintenanceLog).where(
            MaintenanceLog.id == log_id,
            MaintenanceLog.vehicle_id == vehicle_id,
        )
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(log, field, value)
    await db.commit()
    await db.refresh(log)
    return log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_maintenance_log(
    vehicle_id: uuid.UUID,
    log_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    await _get_vehicle(vehicle_id, current_user.id, db)
    result = await db.execute(
        select(MaintenanceLog).where(
            MaintenanceLog.id == log_id,
            MaintenanceLog.vehicle_id == vehicle_id,
        )
    )
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="Maintenance log not found")
    await db.delete(log)
    await db.commit()
