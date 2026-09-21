"""
CyberShield AI
Network Scan API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.services.network_service import start_network_scan

router = APIRouter(
    prefix="/network-scan",
    tags=["Network Scan"],
)

@router.post("/")
def network_scan(
    target: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Network Scan API
    """

    return start_network_scan(
        db=db,
        user_id=current_user.id,
        target=target,
    )
