"""
CyberShield AI
AI Assistant
"""

from app.engines.ai_engine.report_analyzer import analyze_report
from app.engines.ai_engine.prompt_builder import build_prompt
from app.engines.ai_engine.recommendation_engine import generate_recommendations
from app.engines.ai_engine.remediation_generator import generate_remediation

def generate_ai_report(scan_report: dict) -> dict:
    """
    Generate a complete AI security report.
    """

    analysis = analyze_report(scan_report)

    prompt = build_prompt(scan_report)

    recommendations = generate_recommendations(
        scan_report
    )

    remediation = generate_remediation(
        scan_report
    )

    executive_summary = create_summary(
        analysis
    )

    return {

        "status": "Completed",

        "summary": executive_summary,

        "analysis": analysis,

        "recommendations": recommendations,

        "remediation": remediation,

        "llm_prompt": prompt
    }

def create_summary(
    analysis: dict
) -> str:
    """
    Create an executive summary.
    """

    total = analysis.get(
        "total_findings",
        0
    )

    critical = len(
        analysis.get("critical", [])
    )

    high = len(
        analysis.get("high", [])
    )

    medium = len(
        analysis.get("medium", [])
    )

    low = len(
        analysis.get("low", [])
    )

    return (
        f"Scan completed successfully. "
        f"Total findings: {total}. "
        f"Critical: {critical}, "
        f"High: {high}, "
        f"Medium: {medium}, "
        f"Low: {low}."
    )
