"""Generate and persist JSON/PDF reports with database ownership metadata."""

from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.models.report import Report
from app.reports.json_exporter import export_json
from app.reports.pdf_generator import generate_pdf

REPORTS_DIR = Path(__file__).resolve().parents[2] / "reports"

def create_persisted_report(
    db: Session,
    user_id: int,
    report_type: str,
    report: dict[str, Any],
    stem: str,
) -> Report:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORTS_DIR / f"{stem}.json"
    pdf_path = REPORTS_DIR / f"{stem}.pdf"

    export_json(report, json_path)
    generate_pdf(report, str(pdf_path))

    record = Report(
        user_id=user_id,
        report_type=report_type,
        file_path=str(pdf_path.resolve()),
        json_file_path=str(json_path.resolve()),
        status="Generated",
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
