from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.services.file_integrity_service import start_file_scan

router = APIRouter(prefix="/file-integrity", tags=["File Integrity"])

@router.post("/")
def file_integrity(
    file_path: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return start_file_scan(db, file_path, current_user.id)
