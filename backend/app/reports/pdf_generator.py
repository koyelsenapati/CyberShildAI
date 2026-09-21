"""
CyberShield AI
Enterprise PDF Generator
"""

from reportlab.platypus import (
    SimpleDocTemplate,
    PageBreak,
)

from app.reports.cover_page import build_cover_page
from app.reports.table_of_contents import build_table_of_contents
from app.reports.executive_summary import build_executive_summary
from app.reports.findings_generator import build_findings
from app.reports.charts import build_charts
from app.reports.recommendation_writer import build_recommendations
from app.reports.remediation_writer import build_remediation
from app.reports.appendix import build_appendix
from app.reports.page_footer import draw_footer

def generate_pdf(
    report: dict,
    filename: str,
):
    """
    Generate Enterprise Security Assessment Report.
    """

    document = SimpleDocTemplate(
        filename,

        title="CyberShield AI Report",

        author="CyberShield AI",

        subject="Security Assessment",

        creator="CyberShield AI",
    )

    story = []

    report_info = {

        "target": report.get(
            "scan_report",
            {}
        ).get(
            "url",
            "Unknown"
        ),

        "generated_at": report.get(
            "metadata",
            {}
        ).get(
            "generated_at",
            "Unknown"
        ),

        "risk_level": report.get(
            "scan_report",
            {}
        ).get(
            "risk_level",
            "Unknown"
        ),
    }

    build_cover_page(
        story,
        report_info
    )

    story.append(
        PageBreak()
    )

    build_table_of_contents(
        story
    )

    story.append(
        PageBreak()
    )

    build_executive_summary(
        story,
        report
    )

    story.append(
        PageBreak()
    )

    build_charts(
        story,
        report
    )

    story.append(
        PageBreak()
    )

    build_findings(
        story,
        report
    )

    story.append(
        PageBreak()
    )

    build_recommendations(
        story,
        report
    )

    story.append(
        PageBreak()
    )

    build_remediation(
        story,
        report
    )

    story.append(
        PageBreak()
    )

    build_appendix(
        story,
        report
    )

    document.build(

        story,

        onFirstPage=draw_footer,

        onLaterPages=draw_footer

    )

    return filename
