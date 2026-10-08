from io import BytesIO
from openpyxl import Workbook

from app.services.reports_service import ReportsService


class ReportExcelService:

    @staticmethod
    def generate():

        data = ReportsService.get_dashboard_data()

        workbook = Workbook()

        sheet = workbook.active

        sheet.title = "RecruitFlow Report"

        # Heading
        sheet["A1"] = "RecruitFlow Analytics Report"

        # Summary
        sheet.append([])
        sheet.append(["Metric", "Value"])

        sheet.append(["Average AI Score", f"{data['average_ai']}%"])
        sheet.append(["Applications", sum(data["monthly_values"])])
        sheet.append(["Pending Offers", data["offer_status"][0]])
        sheet.append(["Accepted Offers", data["offer_status"][1]])
        sheet.append(["Declined Offers", data["offer_status"][2]])
        sheet.append(["Scheduled Interviews", data["interview_status"][0]])
        sheet.append(["Completed Interviews", data["interview_status"][1]])
        sheet.append(["Selected Interviews", data["interview_status"][2]])
        sheet.append(["Rejected Interviews", data["interview_status"][3]])

        # Top Skills
        sheet.append([])
        sheet.append(["Top Skills", "Candidates"])

        for skill, count in data["top_skills"]:
            sheet.append([skill, count])

        # Monthly Applications
        sheet.append([])
        sheet.append(["Month", "Applications"])

        for month, total in zip(
            data["monthly_labels"],
            data["monthly_values"]
        ):
            sheet.append([month, total])

        # Job-wise Applications
        sheet.append([])
        sheet.append(["Job", "Applications"])

        for job, total in zip(
            data["job_labels"],
            data["job_values"]
        ):
            sheet.append([job, total])

        output = BytesIO()

        workbook.save(output)

        output.seek(0)

        return output