from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.schemas.threat_intel import (
    ThreatLookupRequest,
    ThreatLookupResponse,
)
from app.services.threat_intel_service import lookup_threat_indicator

router = APIRouter(
    prefix="/threat-intel",
    tags=["Threat Intelligence"],
)

@router.post(
    "/lookup",
    response_model=ThreatLookupResponse,
)
def threat_lookup(
    payload: ThreatLookupRequest,
    current_user=Depends(get_current_user),
):
    return lookup_threat_indicator(
        indicator=payload.indicator,
        indicator_type=payload.type,
    )
