from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

MasterScanStatus = Literal["Completed", "Partial", "Failed"]

class MasterScanRequest(BaseModel):
    website: str | None = Field(default=None, min_length=1, max_length=500)
    network_target: str | None = Field(default=None, min_length=1, max_length=500)

class MasterScanSummary(BaseModel):
    id: int
    user_id: int
    target: str
    scan_type: str
    risk_level: str
    result: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class MasterScanResponse(BaseModel):
    scan_id: int
    status: MasterScanStatus
    target: str
    risk_level: str
    risk_breakdown: dict[str, Any]

    message: str | None = None

    web_scan: dict[str, Any] | None = None
    network_scan: dict[str, Any] | None = None
    vulnerability: dict[str, Any] | None = None
    phishing: dict[str, Any] | None = None

    report_id: int | None = None
    report_error: str | None = None
    created_at: datetime | None = None

class MasterScanHistoryResponse(BaseModel):
    status: Literal["Success"]
    count: int
    scans: list[MasterScanSummary]
