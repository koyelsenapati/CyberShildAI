"""
CyberShield AI
Table Of Contents
"""

from reportlab.platypus import (
    Paragraph,
    Spacer,
)

from app.reports.templates import (
    get_report_styles
)

def build_table_of_contents(
    story,
):
    """
    Build report TOC.
    """

    styles = get_report_styles()

    story.append(

        Paragraph(

            "Table of Contents",

            styles["heading1"]

        )

    )

    story.append(
        Spacer(1, 20)
    )

    sections = [

        "1. Executive Summary",

        "2. Target Information",

        "3. Risk Analysis",

        "4. Security Findings",

        "5. CVSS Analysis",

        "6. OWASP Mapping",

        "7. AI Recommendations",

        "8. Remediation",

        "9. Appendix"

    ]

    for item in sections:

        story.append(

            Paragraph(

                item,

                styles["body"]

            )

        )

        story.append(
            Spacer(1, 8)
        )

    return story
