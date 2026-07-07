from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

ALLOWED_USER_FIELDS = {
    "first_name", "last_name", "phone", "category", "license_type",
    "license_number", "license_expiry", "address", "city", "postal_code",
    "country", "level",
}


@router.get("/me", response_model=UserRead)
async def read_my_profile(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.patch("/me", response_model=UserRead)
async def update_my_profile(
    update_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    for field, value in update_data.model_dump(exclude_unset=True).items():
        if field not in ALLOWED_USER_FIELDS:
            continue
        setattr(current_user, field, value)
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_account(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Account already deleted")
    current_user.is_active = False
    await db.commit()
