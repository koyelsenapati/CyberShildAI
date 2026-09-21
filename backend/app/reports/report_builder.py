"""
CyberShield AI
Report Builder
"""

from app.engines.ai_engine.assistant import generate_ai_report
from app.reports.report_utils import report_metadata
from app.reports.cvss_calculator import calculate_cvss
from app.reports.owasp_mapping import map_owasp

def build_report(scan_report: dict):
    """
    Build a complete security report.
    """

    # AI Analysis
    ai_report = generate_ai_report(scan_report)

    # CVSS Analysis
    cvss = calculate_cvss(scan_report)

    # OWASP Mapping
    owasp = map_owasp(cvss)

    # Final Report
    return {

        "status": "Completed",

        "metadata": report_metadata(),

        "scan_report": scan_report,

        "ai_report": ai_report,

        "cvss": cvss,

        "owasp": owasp,
    }
