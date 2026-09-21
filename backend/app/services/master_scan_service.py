from sqlalchemy.orm import Session

from app.crud.master_scan import create_master_scan
from app.engines.ai_engine.risk_orchestrator import orchestrate_risk
from app.engines.phishing_engine.phishing_detector import detect_phishing
from app.engines.security_engine.vulnerability_scanner import scan_vulnerabilities
from app.engines.security_engine.web_scan import scan_website
from app.reports.report_builder import build_report
from app.services.report_generation_service import create_persisted_report

def start_master_scan(
    db: Session,
    user_id: int,
    website: str | None = None,
    network_target: str | None = None,
) -> dict:

    target = website or network_target

    if not target:
        return {
            "status": "Failed",
            "message": "No scan target provided.",
        }

    results = {
        "web_scan": None,
        "network_scan": None,
        "vulnerability": None,
        "phishing": None,
    }

    # -----------------------------
    # WEB SCAN
    # -----------------------------

    if website:
        try:
            results["web_scan"] = scan_website(website)
        except Exception as e:
            results["web_scan"] = {
                "status": "Failed",
                "risk_level": "Low",
                "error": str(e),
            }

    # -----------------------------
    # VULNERABILITY SCAN
    # -----------------------------

    try:
        vulnerability_result = scan_vulnerabilities(
            website=website,
            target=network_target or website,
        )

        results["vulnerability"] = vulnerability_result

        if isinstance(vulnerability_result, dict):
            results["network_scan"] = (
                vulnerability_result.get("network_scan")
            )

    except Exception as e:
        results["vulnerability"] = {
            "status": "Failed",
            "risk_level": "Low",
            "error": str(e),
        }

    # -----------------------------
    # PHISHING SCAN
    # -----------------------------

    if website:
        try:
            results["phishing"] = detect_phishing(
                website
            )

        except Exception as e:
            results["phishing"] = {
                "status": "Failed",
                "risk_level": "Low",
                "error": str(e),
            }

    # -----------------------------
    # RISK ORCHESTRATION
    # -----------------------------

    risk_summary = orchestrate_risk(results)

    component_results = [value for value in results.values() if value is not None]
    failed_components = [
        value for value in component_results
        if isinstance(value, dict) and value.get("status") in {"Failed", "Partial"}
    ]
    if not component_results or len(failed_components) == len(component_results):
        final_status = "Failed"
    elif failed_components:
        final_status = "Partial"
    else:
        final_status = "Completed"

    final_result = {
        "target": target,
        "status": final_status,
        "risk_level": risk_summary["overall_risk"],
        "risk_breakdown": risk_summary["risk_breakdown"],
        "web_scan": results["web_scan"],
        "network_scan": results["network_scan"],
        "vulnerability": results["vulnerability"],
        "phishing": results["phishing"],
    }

    # -----------------------------
    # DATABASE SAVE
    # -----------------------------

    scan_data = {
        "user_id": user_id,
        "target": target,
        "scan_type": "Full Scan",
        "risk_level": risk_summary["overall_risk"],
        "result": str(final_result),
    }

    saved_scan = create_master_scan(
        db,
        scan_data,
    )

    final_result["scan_id"] = saved_scan.id
    final_result["created_at"] = saved_scan.created_at

    try:
        report = build_report(final_result)
        persisted_report = create_persisted_report(
            db, user_id, "Master Scan", report, f"master_scan_{saved_scan.id}"
        )
        final_result["report_id"] = persisted_report.id
    except Exception as exc:
        final_result["status"] = "Partial" if final_result["status"] == "Completed" else final_result["status"]
        final_result["report_id"] = None
        final_result["report_error"] = str(exc)

    return final_result
