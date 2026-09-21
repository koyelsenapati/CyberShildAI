from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.schemas.user import UserResponse
from app.services.user_service import (
    get_all_users,
    get_user,
    delete_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get(
    "/",
    response_model=list[UserResponse],
)
def users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_all_users(db)

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = get_user(db, user_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return result

@router.delete("/{user_id}")
def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = delete_user(db, user_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "message": "User deleted successfully",
    }
