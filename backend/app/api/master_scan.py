from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.master_scan import (
    MasterScanResponse,
    MasterScanHistoryResponse,
)
from app.crud.master_scan import (
    get_master_scan,
    get_user_master_scans,
)
from app.services.master_scan_service import start_master_scan

router = APIRouter(
    prefix="/master-scan",
    tags=["Master Scan"],
)

@router.post(
    "/",
    response_model=MasterScanResponse,
)
def master_scan(
    website: str | None = Query(default=None),
    network_target: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not website and not network_target:
        return {
            "scan_id": 0,
            "status": "Failed",
            "message": "Provide website or network_target.",
            "target": "",
            "risk_level": "Unknown",
            "risk_breakdown": {},
            "web_scan": None,
            "network_scan": None,
            "vulnerability": None,
            "phishing": None,
            "report_id": None,
            "report_error": "Provide website or network_target.",
            "created_at": None,
        }

    return start_master_scan(
        db=db,
        user_id=current_user.id,
        website=website,
        network_target=network_target,
    )

@router.get(
    "/history",
    response_model=MasterScanHistoryResponse,
)
def master_scan_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scans = get_user_master_scans(
        db=db,
        user_id=current_user.id,
    )

    return {
        "status": "Success",
        "count": len(scans),
        "scans": [
            {
                "id": scan.id,
                "user_id": scan.user_id,
                "target": scan.target,
                "scan_type": scan.scan_type,
                "risk_level": scan.risk_level,
                "result": scan.result,
                "created_at": scan.created_at,
            }
            for scan in scans
        ],
    }

@router.get("/{scan_id}")
def master_scan_details(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    scan = get_master_scan(
        db=db,
        scan_id=scan_id,
    )

    if not scan:
        raise HTTPException(
            status_code=404,
            detail="Master scan not found",
        )

    if scan.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    return {
        "status": "Success",
        "scan": {
            "id": scan.id,
            "user_id": scan.user_id,
            "target": scan.target,
            "scan_type": scan.scan_type,
            "risk_level": scan.risk_level,
            "result": scan.result,
            "created_at": scan.created_at,
        },
    }
