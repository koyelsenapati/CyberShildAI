"""
CyberShield AI
Charts Generator
"""

from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def build_charts(story, report: dict):
    """
    Build Risk Score Chart.
    """

    styles = getSampleStyleSheet()

    story.append(
        Paragraph(
            "Risk Analysis",
            styles["Heading1"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    score_map = {
        "Low": 25,
        "Medium": 50,
        "High": 75,
        "Critical": 100
    }

    risk = report.get(
        "scan_report",
        {}
    ).get(
        "risk_level",
        "Low"
    )

    score = score_map.get(
        risk,
        0
    )

    drawing = Drawing(
        450,
        250
    )

    chart = VerticalBarChart()

    chart.x = 60
    chart.y = 40

    chart.height = 150
    chart.width = 280

    chart.data = [
        (score,)
    ]

    chart.categoryAxis.categoryNames = [
        risk
    ]

    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 100
    chart.valueAxis.valueStep = 20

    chart.bars[0].fillColor = colors.red

    drawing.add(chart)

    label = Label()

    label.x = 210
    label.y = 210

    label.setText(
        f"Overall Risk Score : {score}/100"
    )

    drawing.add(label)

    story.append(
        drawing
    )

    story.append(
        Spacer(1, 25)
    )

    return story
