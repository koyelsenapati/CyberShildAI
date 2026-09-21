from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.schemas.scan import (
    ScanCreate,
    ScanResponse,
    ScanStatusResponse,
    ScanUpdate,
)
from app.services.scan_service import (
    create_scan,
    get_all_scans,
    get_scan_by_id,
    update_scan_status,
)

router = APIRouter(
    prefix="/scans",
    tags=["Scans"],
)

@router.post(
    "/",
    response_model=ScanResponse,
)
def create_new_scan(
    scan_data: ScanCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_scan(
        db=db,
        user_id=current_user.id,
        scan_type=scan_data.scan_type,
        target=scan_data.target,
    )

@router.get(
    "/",
    response_model=list[ScanResponse],
)
def read_scans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_all_scans(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/{scan_id}",
    response_model=ScanResponse,
)
def read_single_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    scan = get_scan_by_id(
        db=db,
        scan_id=scan_id,
        user_id=current_user.id,
    )

    if not scan:
        raise HTTPException(
            status_code=404,
            detail="Scan not found",
        )

    return scan

@router.patch(
    "/{scan_id}/status",
    response_model=ScanStatusResponse,
)
def update_scan(
    scan_id: int,
    scan_data: ScanUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    scan = update_scan_status(
        db=db,
        scan_id=scan_id,
        status=scan_data.status,
        user_id=current_user.id,
    )

    if not scan:
        raise HTTPException(
            status_code=404,
            detail="Scan not found",
        )

    return scan
