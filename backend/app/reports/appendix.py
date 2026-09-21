"""
CyberShield AI
Technical Appendix
"""

from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from reportlab.lib import colors

from app.reports.templates import (
    get_report_styles
)

def build_appendix(
    story,
    report: dict,
):
    """
    Build Technical Appendix.
    """

    styles = get_report_styles()

    story.append(
        Paragraph(
            "Appendix",
            styles["heading1"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    scan = report.get(
        "scan_report",
        {}
    )

    data = [

        ["Property", "Value"],

        ["Target URL", scan.get("url", "N/A")],

        ["SSL", scan.get("ssl_status", "Unknown")],

        ["Headers", scan.get("security_headers", "Unknown")],

        ["Cookies", scan.get("cookies", "Unknown")],

        ["robots.txt", scan.get("robots", "Unknown")],

        ["Server", scan.get("server", "Unknown")],

        ["Forms", str(scan.get("forms", 0))],

        ["Scripts", str(scan.get("scripts", 0))],

        ["Risk Level", scan.get("risk_level", "Unknown")],

    ]

    table = Table(
        data,
        colWidths=[170, 280]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

            ("BACKGROUND", (0, 1), (0, -1), colors.whitesmoke),

        ])

    )

    story.append(table)

    story.append(
        Spacer(1, 25)
    )

    return story
