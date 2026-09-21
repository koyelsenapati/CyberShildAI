from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.engines.security_engine.password_analyzer import analyze_password
from app.schemas.prd_features import PasswordAnalyzeRequest, PasswordAnalyzeResponse

router = APIRouter(prefix="/password", tags=["Password Security"])

@router.post("/analyze", response_model=PasswordAnalyzeResponse)
def password_analyze(payload: PasswordAnalyzeRequest, current_user=Depends(get_current_user)):
    return analyze_password(payload.password)
