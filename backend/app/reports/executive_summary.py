"""
CyberShield AI
Executive Summary Generator
"""

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer

def build_executive_summary(
    story,
    report: dict,
):
    """
    Build Executive Summary section.
    """

    styles = getSampleStyleSheet()

    title = styles["Heading1"]

    heading = styles["Heading2"]

    normal = styles["BodyText"]

    story.append(
        Paragraph(
            "Executive Summary",
            title
        )
    )

    story.append(
        Spacer(1, 20)
    )

    scan = report.get(
        "scan_report",
        {}
    )

    ai = report.get(
        "ai_report",
        {}
    )

    findings = ai.get(
        "analysis",
        {}
    )

    total = findings.get(
        "total_findings",
        0
    )

    critical = len(
        findings.get(
            "critical",
            []
        )
    )

    high = len(
        findings.get(
            "high",
            []
        )
    )

    medium = len(
        findings.get(
            "medium",
            []
        )
    )

    low = len(
        findings.get(
            "low",
            []
        )
    )

    story.append(
        Paragraph(
            "<b>Assessment Overview</b>",
            heading
        )
    )

    story.append(
        Paragraph(
            (
                "CyberShield AI performed an automated "
                "security assessment of the target "
                "application and infrastructure."
            ),
            normal
        )
    )

    story.append(
        Spacer(1, 15)
    )

    story.append(
        Paragraph(
            f"<b>Target:</b> {scan.get('url','N/A')}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Overall Risk:</b> {scan.get('risk_level','Unknown')}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Total Findings:</b> {total}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Critical:</b> {critical}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>High:</b> {high}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Medium:</b> {medium}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Low:</b> {low}",
            normal
        )
    )

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            (
                "This assessment should be used as a "
                "decision-support document. All critical "
                "and high-risk findings should be addressed "
                "before deploying the application into "
                "production."
            ),
            normal
        )
    )

    story.append(
        Spacer(1, 25)
    )

    return story
