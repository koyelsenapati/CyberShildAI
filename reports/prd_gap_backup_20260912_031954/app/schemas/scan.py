from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class ScanCreate(BaseModel):
    scan_type: str = Field(..., min_length=2, max_length=50)
    target: str = Field(..., min_length=1, max_length=500)

class ScanResponse(BaseModel):
    id: int
    user_id: int
    scan_type: str
    target: str
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ScanUpdate(BaseModel):
    status: str = Field(..., min_length=2, max_length=50)

class ScanStatusResponse(BaseModel):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)
