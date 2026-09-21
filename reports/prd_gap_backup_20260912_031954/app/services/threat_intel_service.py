from __future__ import annotations

from datetime import datetime, timezone
import ipaddress
import re

import requests
from fastapi import HTTPException

from app.core.config import settings

VT_BASE_URL = "https://www.virustotal.com/api/v3"

def _validate_indicator(indicator: str, indicator_type: str) -> str:
    value = indicator.strip()

    if indicator_type == "IP":
        try:
            ipaddress.ip_address(value)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Invalid IP address",
            )

    elif indicator_type == "DOMAIN":
        if (
            len(value) > 253
            or "." not in value
            or not re.fullmatch(
                r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?",
                value,
            )
        ):
            raise HTTPException(
                status_code=422,
                detail="Invalid domain",
            )

    elif indicator_type == "HASH":
        if not re.fullmatch(r"[A-Fa-f0-9]{32}|[A-Fa-f0-9]{40}|[A-Fa-f0-9]{64}", value):
            raise HTTPException(
                status_code=422,
                detail="Invalid file hash",
            )

    return value

def _endpoint(indicator: str, indicator_type: str) -> str:
    if indicator_type == "IP":
        return f"{VT_BASE_URL}/ip_addresses/{indicator}"

    if indicator_type == "DOMAIN":
        return f"{VT_BASE_URL}/domains/{indicator}"

    return f"{VT_BASE_URL}/files/{indicator}"

def _severity(malicious: int, suspicious: int, total: int) -> str:
    if malicious >= 5:
        return "CRITICAL"

    if malicious >= 2:
        return "HIGH"

    if malicious == 1 or suspicious >= 3:
        return "MEDIUM"

    if suspicious > 0:
        return "LOW"

    return "CLEAN"

def _confidence(malicious: int, suspicious: int, total: int) -> float:
    if total <= 0:
        return 0.0

    signal = malicious + suspicious
    return round(min((signal / total) * 100.0, 100.0), 2)

def _reputation_score(attributes: dict, malicious: int, suspicious: int) -> float:
    reputation = attributes.get("reputation")

    if isinstance(reputation, (int, float)):
        # VT community reputation is not a 0-100 score.
        # Normalize it only for the UI's 0-100 representation.
        return round(max(0.0, min(100.0, 50.0 + float(reputation))), 2)

    total = malicious + suspicious
    if total <= 0:
        return 0.0

    return round(max(0.0, min(100.0, (malicious / total) * 100.0)), 2)

def lookup_threat_indicator(indicator: str, indicator_type: str) -> dict:
    api_key = settings.VT_API_KEY

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="Threat intelligence provider is not configured. Set VT_API_KEY.",
        )

    value = _validate_indicator(indicator, indicator_type)

    try:
        response = requests.get(
            _endpoint(value, indicator_type),
            headers={
                "x-apikey": api_key,
                "Accept": "application/json",
            },
            timeout=settings.VT_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail="Threat intelligence provider is unreachable.",
        ) from exc

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Indicator was not found by the threat intelligence provider.",
        )

    if response.status_code in (401, 403):
        raise HTTPException(
            status_code=502,
            detail="Threat intelligence provider rejected the configured API key.",
        )

    if response.status_code == 429:
        raise HTTPException(
            status_code=429,
            detail="Threat intelligence provider rate limit reached.",
        )

    if not response.ok:
        raise HTTPException(
            status_code=502,
            detail=f"Threat intelligence provider returned HTTP {response.status_code}.",
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail="Threat intelligence provider returned invalid JSON.",
        ) from exc

    data = payload.get("data") or {}
    attributes = data.get("attributes") or {}

    stats = attributes.get("last_analysis_stats") or {}

    malicious_count = int(stats.get("malicious", 0) or 0)
    suspicious_count = int(stats.get("suspicious", 0) or 0)
    harmless_count = int(stats.get("harmless", 0) or 0)
    undetected_count = int(stats.get("undetected", 0) or 0)
    timeout_count = int(stats.get("timeout", 0) or 0)

    total = (
        malicious_count
        + suspicious_count
        + harmless_count
        + undetected_count
        + timeout_count
    )

    malicious = malicious_count > 0
    severity = _severity(malicious_count, suspicious_count, total)
    confidence = _confidence(malicious_count, suspicious_count, total)

    last_analysis = attributes.get("last_analysis_date")
    first_submission = attributes.get("first_submission_date")
    last_submission = attributes.get("last_submission_date")

    def iso_timestamp(value):
        if not value:
            return None

        try:
            return datetime.fromtimestamp(
                int(value),
                tz=timezone.utc,
            ).isoformat()
        except (TypeError, ValueError, OSError):
            return None

    description = (
        f"VirusTotal analysis: {malicious_count} malicious, "
        f"{suspicious_count} suspicious, "
        f"{harmless_count} harmless, "
        f"{undetected_count} undetected."
    )

    tags = attributes.get("tags") or []
    if not isinstance(tags, list):
        tags = []

    result = {
        "id": str(data.get("id") or value),
        "indicator": value,
        "type": indicator_type,
        "severity": severity,
        "reputation_score": _reputation_score(
            attributes,
            malicious_count,
            suspicious_count,
        ),
        "malicious": malicious,
        "confidence": confidence,
        "country": attributes.get("country"),
        "provider": "VirusTotal",
        "first_seen": iso_timestamp(first_submission),
        "last_seen": iso_timestamp(last_submission or last_analysis),
        "tags": [str(tag) for tag in tags],
        "description": description,
    }

    return {"indicator": result}
