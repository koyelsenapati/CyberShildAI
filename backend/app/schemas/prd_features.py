from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

class PasswordAnalyzeRequest(BaseModel):
    password: str = Field(min_length=1, max_length=256)

class PasswordAnalyzeResponse(BaseModel):
    score: int = Field(ge=0, le=100)
    strength: str
    entropy: float = Field(ge=0)
    common_password: bool
    brute_force_seconds: float = Field(ge=0)
    suggestions: list[str]

class MalwareHashResponse(BaseModel):
    filename: str | None = None
    sha256: str = Field(pattern=r"^[a-fA-F0-9]{64}$")
    classification: str
    reputation: str
    source: str
    provider: str | None = None

class IncidentCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    severity: str = Field(default="Medium", pattern=r"^(Low|Medium|High|Critical)$")
    description: str | None = Field(default=None, max_length=10000)

class IncidentUpdateRequest(BaseModel):
    status: str | None = Field(default=None, pattern=r"^(Open|Investigating|Resolved|Closed)$")
    analyst_notes: str | None = Field(default=None, max_length=10000)
    resolution: str | None = Field(default=None, max_length=10000)
    severity: str | None = Field(default=None, pattern=r"^(Low|Medium|High|Critical)$")

class IncidentResponse(BaseModel):
    id: int
    user_id: int
    title: str
    severity: str
    status: str
    description: str | None
    analyst_notes: str | None
    resolution: str | None
    created_at: datetime | None
    updated_at: datetime | None
    model_config = ConfigDict(from_attributes=True)

class EmailPhishingResponse(BaseModel):
    sender: str
    subject: str
    links: list[str]
    suspicious_terms: list[str]
    suspicious_links: list[str]
    phishing_probability: int = Field(ge=0, le=100)
    classification: str
