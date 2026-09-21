"""
CyberShield AI
Phishing CRUD
"""

from sqlalchemy.orm import Session

from app.models.phishing import PhishingScan

def create_phishing_scan(db: Session, data: dict):

    scan = PhishingScan(**data)

    db.add(scan)

    db.commit()

    db.refresh(scan)

    return scan

def get_all_scans(db: Session):

    return (
        db.query(PhishingScan)
        .order_by(PhishingScan.id.desc())
        .all()
    )

def get_scan(db: Session, scan_id: int):

    return (
        db.query(PhishingScan)
        .filter(PhishingScan.id == scan_id)
        .first()
    )
