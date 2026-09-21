"""Phishing scan service with persisted JSON/PDF reports."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.phishing import create_phishing_scan
from app.engines.phishing_engine.phishing_detector import detect_phishing
from app.reports.report_builder import build_report
from app.services.report_generation_service import create_persisted_report

def detect_url(db: Session, url: str, user_id: int):
    try:
        result = detect_phishing(url)
        prediction = result.get("ai_prediction", {})
        label = str(prediction.get("label", "Unknown"))
        confidence = float(result.get("confidence", 0.0))
        reputation_info = result.get("reputation", {})
        reputation = (
            reputation_info.get("status")
            if isinstance(reputation_info, dict)
            else str(reputation_info)
        )
        domain_info = result.get("domain_analysis", {})
        domain = (
            domain_info.get("domain")
            if isinstance(domain_info, dict)
            else None
        )
        risk = str(result.get("risk_level", "Unknown"))
        scan = create_phishing_scan(
            db,
            {
                "user_id": user_id,
                "url": url,
                "prediction": label,
                "probability": confidence,
                "confidence_score": round(confidence * 100),
                "verdict": label,
                "domain": domain,
                "reputation": reputation,
                "risk_level": risk,
            },
        )
        report = build_report(result)
        persisted = create_persisted_report(
            db, user_id, "Phishing", report, f"phishing_{scan.id}"
        )
        return {"scan": scan, "report_id": persisted.id}
    except Exception as error:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(error)) from error
