from sqlalchemy.orm import Session

from app.models.scan import Scan

def create_scan(
    db: Session,
    user_id: int,
    scan_type: str,
    target: str,
):
    scan = Scan(
        user_id=user_id,
        scan_type=scan_type,
        target=target,
        status="Pending",
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)

    return scan

def get_all_scans(
    db: Session,
    user_id: int | None = None,
):
    query = db.query(Scan)

    if user_id is not None:
        query = query.filter(
            Scan.user_id == user_id
        )

    return query.all()

def get_scan_by_id(
    db: Session,
    scan_id: int,
    user_id: int | None = None,
):
    query = db.query(Scan).filter(
        Scan.id == scan_id
    )

    if user_id is not None:
        query = query.filter(
            Scan.user_id == user_id
        )

    return query.first()

def update_scan_status(
    db: Session,
    scan_id: int,
    status: str,
    user_id: int | None = None,
):
    scan = get_scan_by_id(
        db=db,
        scan_id=scan_id,
        user_id=user_id,
    )

    if not scan:
        return None

    scan.status = status

    db.commit()
    db.refresh(scan)

    return scan
