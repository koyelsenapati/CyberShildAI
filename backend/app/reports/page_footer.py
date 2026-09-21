"""
CyberShield AI
Page Footer
"""

from reportlab.lib.units import mm

def draw_footer(canvas, doc):
    """
    Draw footer on every page.
    """

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        9
    )

    page = canvas.getPageNumber()

    canvas.drawString(

        20 * mm,

        10 * mm,

        "CyberShield AI"

    )

    canvas.drawRightString(

        190 * mm,

        10 * mm,

        f"Page {page}"

    )

    canvas.restoreState()
