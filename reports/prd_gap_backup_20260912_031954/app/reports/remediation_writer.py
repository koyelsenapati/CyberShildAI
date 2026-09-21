"""
CyberShield AI
Remediation Checklist
"""

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    Spacer,
)

def build_remediation(
    story,
    report: dict,
):
    """
    Build Remediation Checklist.
    """

    styles = getSampleStyleSheet()

    story.append(

        Paragraph(

            "Remediation Checklist",

            styles["Heading1"]

        )

    )

    story.append(
        Spacer(1, 20)
    )

    checklist = [

        "â˜ Enable HTTPS",

        "â˜ Configure HSTS",

        "â˜ Add Content Security Policy",

        "â˜ Enable X-Frame-Options",

        "â˜ Enable X-Content-Type-Options",

        "â˜ Validate User Input",

        "â˜ Use Parameterized Queries",

        "â˜ Escape HTML Output",

        "â˜ Enable CSRF Protection",

        "â˜ Configure Secure Cookies",

        "â˜ Regularly Update Dependencies",

        "â˜ Perform Periodic Vulnerability Scans",

        "â˜ Review Application Logs",

        "â˜ Implement Security Monitoring",

        "â˜ Conduct Annual Penetration Testing"

    ]

    for item in checklist:

        story.append(

            Paragraph(

                item,

                styles["BodyText"]

            )

        )

        story.append(

            Spacer(1, 8)

        )

    return story
