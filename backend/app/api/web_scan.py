from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.web_scan import WebScanCreate, WebScanResponse
from app.services.web_scan_service import scan_url

router = APIRouter(
    prefix="/web-scan",
    tags=["Web Scan"],
)

@router.post("/", response_model=WebScanResponse)
def web_scan(
    payload: WebScanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return scan_url(
        db=db,
        url=str(payload.url),
        user_id=current_user.id,
    )
