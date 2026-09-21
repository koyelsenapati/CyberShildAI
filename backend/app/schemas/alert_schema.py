from datetime import datetime
from pydantic import BaseModel

class AlertCreate(BaseModel):

    title: str
    description: str
    severity: str

class AlertResponse(BaseModel):

    id: int
    user_id: int
    title: str
    description: str
    severity: str
    created_at: datetime

    class Config:
        from_attributes = True
