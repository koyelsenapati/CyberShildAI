"""
CyberShield AI
Phishing Detection Engine

Pipeline:
URL Features
    â†“
Domain Analysis
    â†“
Reputation Check
    â†“
AI Prediction
    â†“
Confidence Calculation
    â†“
Risk Classification
    â†“
Final Phishing Report
"""

from app.engines.phishing_engine.url_features import (
    extract_url_features,
)

from app.engines.phishing_engine.domain_checker import (
    analyze_domain,
)

from app.engines.phishing_engine.reputation_checker import (
    check_reputation,
)

from app.engines.phishing_engine.ai_predictor import (
    predict,
)

from app.engines.phishing_engine.confidence_score import (
    calculate_confidence,
)

def _normalize_prediction(
    prediction: dict | None,
) -> dict:
    """
    Safely normalize AI prediction output.
    """

    if not isinstance(
        prediction,
        dict,
    ):
        return {
            "label": "Unknown",
            "risk_level": "Low",
        }

    return prediction

def _calculate_risk_level(
    ai_prediction: dict,
    confidence: float,
) -> str:
    """
    Determine final phishing risk.

    AI prediction is treated as the primary
    signal. Confidence strengthens the result
    but does not independently create a
    Critical vulnerability.
    """

    prediction_risk = str(
        ai_prediction.get(
            "risk_level",
            "",
        )
    ).strip().lower()

    prediction_label = str(
        ai_prediction.get(
            "label",
            "",
        )
    ).strip().lower()

    # ---------------------------------------------------------
    # Explicit AI risk
    # ---------------------------------------------------------

    if prediction_risk == "critical":
        return "Critical"

    if prediction_risk == "high":
        return "High"

    if prediction_risk == "medium":
        return "Medium"

    # ---------------------------------------------------------
    # Phishing prediction + confidence
    # ---------------------------------------------------------

    is_phishing = prediction_label in {
        "phishing",
        "malicious",
        "suspicious",
    }

    if is_phishing:

        if confidence >= 0.90:
            return "Critical"

        if confidence >= 0.75:
            return "High"

        if confidence >= 0.50:
            return "Medium"

        return "Low"

    # ---------------------------------------------------------
    # Safe / benign prediction
    # ---------------------------------------------------------

    if prediction_label in {
        "safe",
        "benign",
        "legitimate",
    }:
        return "Low"

    return "Low"

def detect_phishing(
    url: str,
) -> dict:
    """
    Complete phishing detection pipeline.

    Steps:
        1. Extract URL features
        2. Analyze domain
        3. Check reputation
        4. Run AI prediction
        5. Calculate confidence
        6. Determine risk
        7. Return structured report
    """

    # =========================================================
    # STEP 1 â€” URL FEATURES
    # =========================================================

    url_features = extract_url_features(
        url
    )

    # =========================================================
    # STEP 2 â€” DOMAIN ANALYSIS
    # =========================================================

    domain_info = analyze_domain(
        url
    )

    # Make sure domain_info is a dict.
    if not isinstance(
        domain_info,
        dict,
    ):
        domain_info = {
            "domain": "",
            "status": "Unknown",
        }

    domain = domain_info.get(
        "domain",
        "",
    )

    # =========================================================
    # STEP 3 â€” REPUTATION CHECK
    # =========================================================

    reputation = check_reputation(
        domain
    )

    if not isinstance(
        reputation,
        dict,
    ):
        reputation = {
            "status": "Unknown",
        }

    # =========================================================
    # STEP 4 â€” AI PREDICTION
    # =========================================================

    ai_prediction = predict(
        url_features
    )

    ai_prediction = _normalize_prediction(
        ai_prediction
    )

    # =========================================================
    # STEP 5 â€” CONFIDENCE
    # =========================================================

    confidence = calculate_confidence(
        url_features=url_features,
        domain_info=domain_info,
        reputation=reputation,
        ai_prediction=ai_prediction,
    )

    # Protect against invalid confidence.
    if not isinstance(
        confidence,
        (int, float),
    ):
        confidence = 0.0

    confidence = max(
        0.0,
        min(
            float(confidence),
            1.0,
        ),
    )

    # =========================================================
    # STEP 6 â€” FINAL RISK
    # =========================================================

    risk_level = _calculate_risk_level(
        ai_prediction=ai_prediction,
        confidence=confidence,
    )

    # =========================================================
    # STEP 7 â€” FINAL REPORT
    # =========================================================

    report = {
        "status": "Completed",

        "url": url,

        "risk_level": risk_level,

        "is_phishing": (
            risk_level
            in {
                "High",
                "Critical",
            }
        ),

        "confidence": round(
            confidence,
            4,
        ),

        "url_features": url_features,

        "domain_analysis": domain_info,

        "reputation": reputation,

        "ai_prediction": ai_prediction,
    }

    return report
