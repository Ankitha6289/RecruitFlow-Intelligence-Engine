from flask import Blueprint, render_template, session, redirect, url_for, request

from app.services.report_service import ReportService
from openpyxl import Workbook
from flask import send_file
import io
report_bp = Blueprint("report", __name__)


@report_bp.route("/reports")
def reports():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "")

    candidates = ReportService.get_all_candidates(search)

    return render_template(
        "reports.html",
        candidates=candidates,
        search=search
    )
@report_bp.route("/reports/excel")
def export_excel():

    wb = Workbook()

    ws = wb.active

    ws.title = "Candidates"

    ws.append([
        "ID",
        "Name",
        "Email",
        "Phone"
    ])

    candidates = ReportService.get_all_candidates()

    for c in candidates:

        ws.append([
            c.candidate_id,
            c.full_name,
            c.email,
            c.phone
        ])

    output = io.BytesIO()

    wb.save(output)

    output.seek(0)

    return send_file(
        output,
        download_name="Candidate_Report.xlsx",
        as_attachment=True
    )
@report_bp.route("/reports")
def reports():

    candidates = ReportService.get_all_candidates()

    print("Candidates:", candidates)

    return render_template(
        "reports.html",
        candidates=candidates
    )