"""
CyberShield AI
Report Templates
"""

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def get_report_styles():
    """
    Returns all report styles.
    """

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.fontName = "Helvetica-Bold"
    title.fontSize = 24
    title.leading = 30
    title.textColor = colors.darkblue

    heading1 = styles["Heading1"]
    heading1.fontName = "Helvetica-Bold"
    heading1.fontSize = 18
    heading1.leading = 24
    heading1.textColor = colors.darkblue

    heading2 = styles["Heading2"]
    heading2.fontName = "Helvetica-Bold"
    heading2.fontSize = 14
    heading2.leading = 20
    heading2.textColor = colors.navy

    body = styles["BodyText"]
    body.fontName = "Helvetica"
    body.fontSize = 10
    body.leading = 16

    return {

        "title": title,

        "heading1": heading1,

        "heading2": heading2,

        "body": body
    }
