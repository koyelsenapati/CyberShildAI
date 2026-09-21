from pydantic import BaseModel, ConfigDict

class AlertCreate(BaseModel):
    title: str
    description: str
    severity: str

class AlertResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    status: str

    model_config = ConfigDict(from_attributes=True)

