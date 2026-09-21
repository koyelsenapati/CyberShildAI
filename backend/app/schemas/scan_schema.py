from datetime import datetime
from pydantic import BaseModel

class ScanCreate(BaseModel):

    scan_type: str
    target: str

class ScanResponse(BaseModel):

    id: int
    user_id: int
    scan_type: str
    target: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
