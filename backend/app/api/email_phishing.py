from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from app.api.dependencies import get_current_user
from app.engines.security_engine.email_phishing import analyze_email
from app.schemas.prd_features import EmailPhishingResponse

router = APIRouter(prefix="/email-phishing", tags=["Email Phishing"])
MAX_EMAIL_BYTES = 2 * 1024 * 1024

@router.post("/analyze", response_model=EmailPhishingResponse)
async def analyze_email_file(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    content = await file.read(MAX_EMAIL_BYTES + 1)
    if len(content) > MAX_EMAIL_BYTES:
        raise HTTPException(status_code=413, detail="Email file exceeds the 2 MiB limit.")
    try:
        return analyze_email(content)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid email file.") from exc
