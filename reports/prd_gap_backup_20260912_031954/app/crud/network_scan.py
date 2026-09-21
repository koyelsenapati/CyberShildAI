"""
CyberShield AI
Network Scan CRUD
"""

from sqlalchemy.orm import Session

from app.models.network_scan import NetworkScan

def create_network_scan(db: Session, data: dict):
    scan = NetworkScan(**data)
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan

def get_network_scan(db: Session, scan_id: int):
    return (
        db.query(NetworkScan)
        .filter(NetworkScan.id == scan_id)
        .first()
    )

def get_all_network_scans(db: Session):
    return (
        db.query(NetworkScan)
        .order_by(NetworkScan.id.desc())
        .all()
    )

def delete_network_scan(db: Session, scan_id: int):
    scan = get_network_scan(db, scan_id)

    if scan:
        db.delete(scan)
        db.commit()

    return scan
