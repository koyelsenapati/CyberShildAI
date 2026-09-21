"""
CyberShield AI
Web Scan API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.services.web_scan_service import scan_url

router = APIRouter(
    prefix="/web-scan",
    tags=["Web Scan"],
)

@router.post("/")
def web_scan(
    url: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return scan_url(
        db=db,
        user_id=current_user.id,
        url=url,
    )
