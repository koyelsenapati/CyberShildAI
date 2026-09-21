from typing import Literal

from pydantic import BaseModel, Field, field_validator

IndicatorType = Literal["IP", "DOMAIN", "HASH"]
ThreatSeverity = Literal["CLEAN", "LOW", "MEDIUM", "HIGH", "CRITICAL"]

class ThreatLookupRequest(BaseModel):
    indicator: str = Field(min_length=1, max_length=255)
    type: IndicatorType

    @field_validator("indicator")
    @classmethod
    def normalize_indicator(cls, value: str) -> str:
        return value.strip()

class ThreatIndicator(BaseModel):
    id: str
    indicator: str
    type: IndicatorType
    severity: ThreatSeverity
    reputation_score: float
    malicious: bool
    confidence: float
    country: str | None = None
    provider: str
    first_seen: str | None = None
    last_seen: str | None = None
    tags: list[str] = []
    description: str

class ThreatLookupResponse(BaseModel):
    indicator: ThreatIndicator
