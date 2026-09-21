from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.file_integrity import create_file_scan
from app.engines.security_engine.file_integrity import calculate_hash

def start_file_scan(
    db: Session,
    file_path: str,
    user_id: int,
):
    """Calculate a SHA-256 hash and persist it for the requesting user."""
    try:
        result = calculate_hash(file_path)
        scan = create_file_scan(
            db,
            {
                "user_id": user_id,
                "file_path": result["file"],
                "file_hash": result["hash"],
                "algorithm": result["algorithm"],
                "status": "Safe",
                "result": str(result),
            },
        )
        return {"message": "File Integrity Scan Completed", "scan": scan}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
