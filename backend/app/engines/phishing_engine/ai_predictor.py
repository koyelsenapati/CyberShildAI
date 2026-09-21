"""
CyberShield AI
AI Predictor
"""

from pathlib import Path

import joblib

MODEL_PATH = (
    Path(__file__).parent.parent
    / "ml_models"
    / "phishing_model.joblib"
)

_model = None

def load_model():
    """
    Load ML model only once.
    """

    global _model

    if _model is None:

        if MODEL_PATH.exists():

            _model = joblib.load(MODEL_PATH)

        else:

            _model = None

    return _model

def prepare_features(features: dict) -> list:
    """
    Convert feature dictionary into ML input vector.

    IMPORTANT:
    Keep this order identical to the training dataset.
    """

    return [
        features.get("length", 0),
        features.get("path_length", 0),
        int(features.get("uses_https", False)),
        int(features.get("contains_ip", False)),
        int(features.get("contains_at", False)),
        int(features.get("contains_dash", False)),
        features.get("subdomain_count", 0),
        features.get("digit_count", 0),
        features.get("special_char_count", 0),
        int(features.get("is_shortened", False)),
        features.get("suspicious_word_count", 0),
    ]

def predict(features: dict) -> dict:
    """
    Predict whether a URL is phishing.
    """

    model = load_model()

    if model is None:

        return {
            "prediction": "Unknown",
            "probability": 0.0,
            "confidence": 0.0,
            "risk_level": "Low",
            "message": "Model not found.",
        }

    try:

        vector = prepare_features(features)

        probabilities = model.predict_proba([vector])[0]

        phishing_probability = float(
            probabilities[1]
        )

        prediction = (
            "Phishing"
            if phishing_probability >= 0.50
            else "Legitimate"
        )

        confidence = round(
            phishing_probability,
            4,
        )

        if phishing_probability >= 0.90:
            risk_level = "Critical"

        elif phishing_probability >= 0.75:
            risk_level = "High"

        elif phishing_probability >= 0.50:
            risk_level = "Medium"

        else:
            risk_level = "Low"

        return {
            "prediction": prediction,
            "probability": phishing_probability,
            "confidence": confidence,
            "risk_level": risk_level,
        }

    except Exception as e:

        return {
            "prediction": "Unknown",
            "probability": 0.0,
            "confidence": 0.0,
            "risk_level": "Low",
            "message": str(e),
        }
