from sqlalchemy.orm import Session

from app.models.file_integrity import FileIntegrity

def create_file_scan(db: Session, data: dict):

    scan = FileIntegrity(**data)

    db.add(scan)
    db.commit()
    db.refresh(scan)

    return scan

def get_file_scan(db: Session, scan_id:int):

    return (
        db.query(FileIntegrity)
        .filter(FileIntegrity.id == scan_id)
        .first()
    )
