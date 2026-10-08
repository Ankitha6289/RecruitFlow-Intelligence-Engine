from flask import (
    Blueprint,
    session,
    redirect,
    url_for,
    send_file
)

from app.services.report_pdf_service import ReportPDFService
from app.services.report_excel_service import ReportExcelService


report_export_bp = Blueprint(
    "report_export",
    __name__
)


# ==========================================
# Export PDF Report
# ==========================================

@report_export_bp.route("/admin/reports/pdf")
def export_pdf():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    pdf = ReportPDFService.generate()

    return send_file(

        pdf,

        download_name="RecruitFlow_Report.pdf",

        as_attachment=True,

        mimetype="application/pdf"

    )


# ==========================================
# Export Excel Report
# ==========================================

@report_export_bp.route("/admin/reports/excel")
def export_excel():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    excel = ReportExcelService.generate()

    return send_file(

        excel,

        download_name="RecruitFlow_Report.xlsx",

        as_attachment=True,

        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )