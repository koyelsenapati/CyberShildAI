from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
