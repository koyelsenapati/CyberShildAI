"""
CyberShield AI
Central Risk Orchestrator

Responsible for:
- Normalizing risk levels
- Comparing scanner risks
- Calculating Master Scan risk
- Building risk breakdown
- Providing a unified risk summary
"""

from typing import Any

RISK_ORDER = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4,
}

VALID_RISKS = set(RISK_ORDER.keys())

def normalize_risk(risk: Any) -> str:
    """
    Normalize any risk value into a valid
    CyberShield AI risk level.
    """

    if risk is None:
        return "Low"

    risk = str(risk).strip().lower()

    risk_mapping = {
        "low": "Low",
        "medium": "Medium",
        "moderate": "Medium",
        "high": "High",
        "critical": "Critical",
    }

    return risk_mapping.get(
        risk,
        "Low",
    )

def get_highest_risk(
    *risks: str | None,
) -> str:
    """
    Return the highest risk level
    from multiple risk values.
    """

    highest = "Low"

    for risk in risks:

        normalized = normalize_risk(
            risk
        )

        if (
            RISK_ORDER[normalized]
            > RISK_ORDER[highest]
        ):
            highest = normalized

    return highest

def calculate_master_risk(
    web_result: dict | None = None,
    network_result: dict | None = None,
    phishing_result: dict | None = None,
    vulnerability_result: dict | None = None,
) -> str:
    """
    Calculate the overall Master Scan risk.

    The highest valid risk from all
    security engines becomes the
    overall risk.
    """

    risks = []

    # ---------------------------------------------------------
    # WEB SCAN
    # ---------------------------------------------------------

    if web_result:

        risks.append(
            web_result.get(
                "risk_level"
            )
        )

    # ---------------------------------------------------------
    # NETWORK SCAN
    # ---------------------------------------------------------

    if network_result:

        risks.append(
            network_result.get(
                "risk_level"
            )
        )

    # ---------------------------------------------------------
    # VULNERABILITY SCAN
    # ---------------------------------------------------------

    if vulnerability_result:

        risks.append(
            vulnerability_result.get(
                "overall_risk",
                vulnerability_result.get(
                    "risk_level"
                ),
            )
        )

    # ---------------------------------------------------------
    # PHISHING SCAN
    # ---------------------------------------------------------

    phishing_confidence = None

    if phishing_result:

        phishing_risk = phishing_result.get(
            "risk_level"
        )

        risks.append(
            phishing_risk
        )

        # Preserve confidence for
        # metadata/reporting purposes.
        confidence = phishing_result.get(
            "confidence"
        )

        if isinstance(
            confidence,
            (int, float),
        ):
            phishing_confidence = max(
                0.0,
                min(
                    float(confidence),
                    1.0,
                ),
            )

    # ---------------------------------------------------------
    # FINAL RISK
    # ---------------------------------------------------------

    return get_highest_risk(
        *risks
    )

def build_risk_summary(
    web_result: dict | None = None,
    network_result: dict | None = None,
    phishing_result: dict | None = None,
    vulnerability_result: dict | None = None,
) -> dict:
    """
    Build a structured risk summary
    for the Master Scan.
    """

    overall_risk = calculate_master_risk(
        web_result=web_result,
        network_result=network_result,
        phishing_result=phishing_result,
        vulnerability_result=vulnerability_result,
    )

    # ---------------------------------------------------------
    # Individual Risk Levels
    # ---------------------------------------------------------

    web_risk = normalize_risk(
        web_result.get("risk_level")
        if web_result
        else None
    )

    network_risk = normalize_risk(
        network_result.get("risk_level")
        if network_result
        else None
    )

    vulnerability_risk = normalize_risk(
        (
            vulnerability_result.get(
                "overall_risk"
            )
            if vulnerability_result
            else None
        )
    )

    phishing_risk = normalize_risk(
        phishing_result.get("risk_level")
        if phishing_result
        else None
    )

    # ---------------------------------------------------------
    # Phishing Confidence
    # ---------------------------------------------------------

    phishing_confidence = None

    if phishing_result:

        confidence = phishing_result.get(
            "confidence"
        )

        if isinstance(
            confidence,
            (int, float),
        ):

            phishing_confidence = round(
                max(
                    0.0,
                    min(
                        float(confidence),
                        1.0,
                    ),
                ),
                4,
            )

    # ---------------------------------------------------------
    # Risk Score
    # ---------------------------------------------------------

    risk_score = RISK_ORDER[
        overall_risk
    ]

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    return {
        "overall_risk": overall_risk,

        "risk_score": risk_score,

        "risk_breakdown": {
            "web": web_risk,
            "network": network_risk,
            "vulnerability": vulnerability_risk,
            "phishing": phishing_risk,
        },

        "phishing_confidence": (
            phishing_confidence
        ),
    }

def orchestrate_risk(
    results: dict,
) -> dict:
    """
    Central risk orchestration for
    CyberShield AI Master Scan.
    """

    if not isinstance(
        results,
        dict,
    ):
        return {
            "overall_risk": "Low",
            "risk_score": 1,
            "risk_breakdown": {
                "web": "Low",
                "network": "Low",
                "vulnerability": "Low",
                "phishing": "Low",
            },
            "phishing_confidence": None,
        }

    web_result = results.get(
        "web_scan"
    )

    network_result = results.get(
        "network_scan"
    )

    vulnerability_result = results.get(
        "vulnerability"
    )

    phishing_result = results.get(
        "phishing"
    )

    return build_risk_summary(
        web_result=web_result,
        network_result=network_result,
        phishing_result=phishing_result,
        vulnerability_result=vulnerability_result,
    )
