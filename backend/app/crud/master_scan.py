from sqlalchemy.orm import Session

from app.models.master_scan import MasterScan

def create_master_scan(
    db: Session,
    data: dict,
):
    scan = MasterScan(**data)

    db.add(scan)
    db.commit()
    db.refresh(scan)

    return scan

def get_master_scan(
    db: Session,
    scan_id: int,
):
    return (
        db.query(MasterScan)
        .filter(MasterScan.id == scan_id)
        .first()
    )

def get_user_master_scans(
    db: Session,
    user_id: int,
):
    return (
        db.query(MasterScan)
        .filter(MasterScan.user_id == user_id)
        .order_by(MasterScan.created_at.desc())
        .all()
    )
