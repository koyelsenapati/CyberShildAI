"""
CyberShield AI
Recommendation Writer
"""

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    Spacer,
)

def build_recommendations(
    story,
    report: dict,
):
    """
    Build Recommendations section.
    """

    styles = getSampleStyleSheet()

    story.append(
        Paragraph(
            "Security Recommendations",
            styles["Heading1"],
        )
    )

    story.append(
        Spacer(1, 20)
    )

    scan = report.get(
        "scan_report",
        {}
    )

    recommendations = []

    if scan.get("ssl_status") != "Valid":

        recommendations.append(
            (
                "Enable HTTPS with a trusted SSL/TLS certificate."
            )
        )

    if scan.get("security_headers") != "Good":

        recommendations.append(
            (
                "Implement security headers "
                "(CSP, HSTS, X-Frame-Options, "
                "X-Content-Type-Options, Referrer-Policy)."
            )
        )

    if scan.get("sql_injection") == "Possible SQL Injection":

        recommendations.append(
            (
                "Use parameterized SQL queries "
                "or ORM prepared statements."
            )
        )

    if scan.get("xss") == "Possible XSS":

        recommendations.append(
            (
                "Sanitize user input and "
                "encode all output before rendering."
            )
        )

    if scan.get("csrf") == "Possible Missing CSRF":

        recommendations.append(
            (
                "Implement CSRF tokens "
                "for every sensitive form."
            )
        )

    if scan.get("cookies") == "Weak":

        recommendations.append(
            (
                "Enable Secure, HttpOnly "
                "and SameSite cookie attributes."
            )
        )

    if not recommendations:

        recommendations.append(
            "No critical recommendations generated."
        )

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        story.append(

            Paragraph(

                f"<b>{index}.</b> {recommendation}",

                styles["BodyText"]

            )

        )

        story.append(
            Spacer(1, 10)
        )

    return story
