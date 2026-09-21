from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import (
    get_dashboard,
    get_dashboard_statistics,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

@router.get(
    "/",
    response_model=DashboardResponse,
)
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_dashboard(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/statistics",
)
def dashboard_statistics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_dashboard_statistics(
        db=db,
        user_id=current_user.id,
    )
