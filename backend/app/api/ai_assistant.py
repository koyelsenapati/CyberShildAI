from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.schemas.ai_assistant import AIChatRequest, AIChatResponse
from app.services.ai_assistant_service import ask_ai

router = APIRouter(
    prefix="/ai-assistant",
    tags=["AI Assistant"],
)

@router.post(
    "/chat",
    response_model=AIChatResponse,
)
def chat(
    payload: AIChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return ask_ai(
        db=db,
        user_id=current_user.id,
        message=payload.message,
    )
