from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.services.report_service import get_report_file

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/pdf/{report_id}")
def pdf_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    path = get_report_file(db, report_id, current_user.id, ".pdf")
    return FileResponse(path, media_type="application/pdf", filename=path.name)

@router.get("/json/{report_id}")
def json_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    path = get_report_file(db, report_id, current_user.id, ".json")
    return FileResponse(path, media_type="application/json", filename=path.name)
