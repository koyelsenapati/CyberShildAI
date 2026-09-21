from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.crud.alert import create_alert, get_alerts
from app.database.database import get_db
from app.models.user import User
from app.schemas.alert import AlertCreate, AlertResponse

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.post("/", response_model=AlertResponse)
def add_alert(
    data: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_alert(db, data, current_user.id)

@router.get("/", response_model=list[AlertResponse])
def all_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_alerts(db, current_user.id)
