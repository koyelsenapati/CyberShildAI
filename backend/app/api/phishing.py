"""
CyberShield AI
Phishing API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.phishing_service import detect_url
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/phishing",
    tags=["Phishing"],
)

@router.post("/")
def phishing_scan(
    url: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return detect_url(
        db=db,
        url=url,
        user_id=current_user.id,
    )
