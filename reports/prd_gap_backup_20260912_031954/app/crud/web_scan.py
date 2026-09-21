import json

from sqlalchemy.orm import Session

from app.models.web_scan import WebScan

def create_scan(db: Session, data: dict):

    scan = WebScan(**data)

    db.add(scan)
    db.commit()
    db.refresh(scan)

    return scan

def get_scan(db: Session, scan_id: int):

    return (
        db.query(WebScan)
        .filter(WebScan.id == scan_id)
        .first()
    )

def get_all_scans(db: Session):

    return (
        db.query(WebScan)
        .order_by(WebScan.id.desc())
        .all()
    )

def delete_scan(db: Session, scan_id: int):

    scan = get_scan(db, scan_id)

    if scan:
        db.delete(scan)
        db.commit()

    return scan
