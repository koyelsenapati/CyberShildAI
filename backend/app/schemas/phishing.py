from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import HttpUrl

class PhishingScanCreate(BaseModel):
    """
    Request Schema
    """

    url: HttpUrl

class PhishingScanBase(BaseModel):
    """
    Shared Fields
    """

    url: str

    prediction: str

    probability: float

    confidence_score: int

    verdict: str

    domain: str | None = None

    reputation: str | None = None

    risk_level: str

class PhishingScanResponse(
    PhishingScanBase
):
    """
    Response Schema
    """

    id: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
