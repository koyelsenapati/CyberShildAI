"""
CyberShield AI
Confidence Score Calculator
"""

def calculate_confidence(
    url_features: dict,
    domain_info: dict,
    reputation: dict,
    ai_prediction: dict,
) -> float:
    """
    Calculate overall phishing confidence score.

    Returns:
        float: Confidence score between 0.0 and 1.0
    """

    score = 0.0

    # =========================================================
    # URL FEATURES
    # =========================================================

    if not url_features.get("uses_https", True):
        score += 10

    if url_features.get("contains_ip", False):
        score += 20

    suspicious_words = url_features.get(
        "suspicious_word_count",
        0,
    )

    if isinstance(suspicious_words, (int, float)):
        score += suspicious_words * 4

    if url_features.get("is_shortened", False):
        score += 10

    subdomain_count = url_features.get(
        "subdomain_count",
        0,
    )

    if isinstance(subdomain_count, (int, float)):
        if subdomain_count >= 3:
            score += 8

    # =========================================================
    # DOMAIN ANALYSIS
    # =========================================================

    domain_status = str(
        domain_info.get(
            "status",
            "",
        )
    ).strip().lower()

    if domain_status == "suspicious":
        score += 20

    # =========================================================
    # REPUTATION
    # =========================================================

    reputation_status = str(
        reputation.get(
            "reputation",
            "",
        )
    ).strip().lower()

    if reputation_status == "suspicious":
        score += 15

    # =========================================================
    # AI PREDICTION
    # =========================================================

    prediction = str(
        ai_prediction.get(
            "prediction",
            ai_prediction.get(
                "label",
                "",
            ),
        )
    ).strip().lower()

    probability = ai_prediction.get(
        "probability",
        ai_prediction.get(
            "confidence",
            0,
        ),
    )

    if not isinstance(
        probability,
        (int, float),
    ):
        probability = 0.0

    probability = max(
        0.0,
        min(
            float(probability),
            1.0,
        ),
    )

    if prediction in {
        "phishing",
        "malicious",
        "suspicious",
    }:
        score += probability * 30

    # =========================================================
    # NORMALIZE
    # =========================================================

    score = max(
        0.0,
        min(
            score,
            100.0,
        ),
    )

    # Convert 0–100 ? 0.0–1.0
    confidence = score / 100.0

    return round(
        confidence,
        4,
    )
