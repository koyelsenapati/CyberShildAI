"""
CyberShield AI
Enterprise Findings Generator
"""

from reportlab.lib import colors

from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from app.reports.templates import (
    get_report_styles
)

def build_findings(
    story,
    report: dict,
):
    """
    Build Findings Section.
    """

    styles = get_report_styles()

    story.append(

        Paragraph(

            "Detailed Findings",

            styles["heading1"]

        )

    )

    story.append(
        Spacer(1, 20)
    )

    data = [

        [

            "Finding",

            "CVSS",

            "Severity",

            "OWASP"

        ]

    ]

    cvss = report.get(
        "cvss",
        []
    )

    owasp = {

        item["name"]: item["category"]

        for item in report.get(
            "owasp",
            []
        )

    }

    for finding in cvss:

        data.append(

            [

                finding["name"],

                str(finding["cvss"]),

                finding["severity"],

                owasp.get(

                    finding["name"],

                    "-"

                )

            ]

        )

    table = Table(

        data,

        colWidths=[170, 70, 90, 170]

    )

    style = TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ("ALIGN", (1, 1), (-1, -1), "CENTER"),

    ])

    for row in range(
        1,
        len(data)
    ):

        severity = data[row][2]

        if severity == "Critical":

            color = colors.red

        elif severity == "High":

            color = colors.orange

        elif severity == "Medium":

            color = colors.yellow

        else:

            color = colors.lightgreen

        style.add(

            "BACKGROUND",

            (2, row),

            (2, row),

            color

        )

    table.setStyle(style)

    story.append(table)

    story.append(
        Spacer(1, 30)
    )

    return story
