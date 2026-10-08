from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from app.services.reports_service import ReportsService


class ReportPDFService:

    @staticmethod
    def generate():

        data = ReportsService.get_dashboard_data()

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "<b>RecruitFlow Analytics Report</b>",
                styles["Title"]
            )
        )

        elements.append(Spacer(1, 20))

        table_data = [

            ["Metric", "Value"],

            ["Average AI Score",
             f"{data['average_ai']}%"],

            ["Applications",
             sum(data["monthly_values"])],

            ["Pending Offers",
             data["offer_status"][0]],

            ["Accepted Offers",
             data["offer_status"][1]],

            ["Declined Offers",
             data["offer_status"][2]],

            ["Scheduled Interviews",
             data["interview_status"][0]],

            ["Completed Interviews",
             data["interview_status"][1]],

            ["Selected Interviews",
             data["interview_status"][2]],

            ["Rejected Interviews",
             data["interview_status"][3]]

        ]

        table = Table(table_data)

        table.setStyle(

            TableStyle([

                ("BACKGROUND",
                 (0, 0),
                 (-1, 0),
                 colors.darkblue),

                ("TEXTCOLOR",
                 (0, 0),
                 (-1, 0),
                 colors.white),

                ("GRID",
                 (0, 0),
                 (-1, -1),
                 1,
                 colors.black),

                ("BACKGROUND",
                 (0, 1),
                 (-1, -1),
                 colors.beige),

                ("ALIGN",
                 (0, 0),
                 (-1, -1),
                 "CENTER")

            ])

        )

        elements.append(table)

        elements.append(Spacer(1, 20))

        elements.append(

            Paragraph(
                "<b>Top Skills</b>",
                styles["Heading2"]
            )

        )

        for skill, count in data["top_skills"]:

            elements.append(

                Paragraph(
                    f"{skill} : {count}",
                    styles["BodyText"]
                )

            )

        doc.build(elements)

        buffer.seek(0)

        return buffer