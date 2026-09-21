from pydantic import BaseModel, ConfigDict

class DashboardResponse(BaseModel):
    security_score: int
    total_scans: int
    total_alerts: int
    total_vulnerabilities: int
    status: str

    model_config = ConfigDict(from_attributes=True)
