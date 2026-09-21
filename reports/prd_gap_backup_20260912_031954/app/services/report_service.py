from pathlib import Path

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.report import Report

def get_report_file(
    db: Session,
    report_id: int,
    user_id: int,
    suffix: str,
) -> Path:
    report = db.query(Report).filter(Report.id == report_id).first()

    if report is None or report.user_id != user_id:
        raise HTTPException(status_code=404, detail="Report not found")

    stored_path = report.json_file_path if suffix == ".json" else report.file_path
    if not stored_path:
        raise HTTPException(status_code=404, detail="Report file not found")

    file_path = Path(stored_path)
    if file_path.suffix.lower() != suffix or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Report file not found")

    return file_path
