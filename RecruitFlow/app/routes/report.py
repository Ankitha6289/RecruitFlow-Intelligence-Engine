from flask import (
    Blueprint,
    render_template,
    request,
    send_file,
    session
)

import pandas as pd
from io import BytesIO

from app.services.report_service import ReportService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService

report_bp = Blueprint(
    "report",
    __name__
)


# =====================================================
# Reports Dashboard
# =====================================================

@report_bp.route("/reports")
def reports():

    search = request.args.get("search", "")

    candidates = ReportService.get_all_candidates(search)

    return render_template(
        "reports.html",
        candidates=candidates,
        search=search
    )


# =====================================================
# Candidate PDF
# =====================================================

@report_bp.route("/candidate/<int:candidate_id>/pdf")
def export_pdf(candidate_id):

    pdf = ReportService.generate_candidate_pdf(candidate_id)

    if pdf is None:
        return "Candidate Not Found"

    if "user_id" in session:

        ActivityLogService.create(

            session["user_id"],

            "Candidate Report Downloaded",

            "Reports"

        )

    NotificationService.create(

        title="Candidate Report",

        message="Candidate PDF generated successfully.",

        notification_type="Reports",

        recipient_role="Admin"

    )

    return send_file(

        pdf,

        download_name=f"candidate_{candidate_id}.pdf",

        as_attachment=True,

        mimetype="application/pdf"

    )


# =====================================================
# Excel Report
# =====================================================

@report_bp.route("/reports/excel")
def export_excel():

    candidates = ReportService.get_all_candidates()

    data = []

    for c in candidates:

        data.append({

            "ID": c.candidate_id,

            "Name": c.full_name,

            "Email": c.email,

            "Phone": c.phone,

            "LinkedIn": c.linkedin,

            "GitHub": c.github,

            "Portfolio": c.portfolio,

            "Status": c.status

        })

    df = pd.DataFrame(data)

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(

            writer,

            index=False,

            sheet_name="Candidates"

        )

    output.seek(0)

    if "user_id" in session:

        ActivityLogService.create(

            session["user_id"],

            "Candidate Excel Report Downloaded",

            "Reports"

        )

    NotificationService.create(

        title="Excel Report",

        message="Candidate Excel report generated successfully.",

        notification_type="Reports",

        recipient_role="Admin"

    )

    return send_file(

        output,

        download_name="Candidate_Report.xlsx",

        as_attachment=True,

        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )