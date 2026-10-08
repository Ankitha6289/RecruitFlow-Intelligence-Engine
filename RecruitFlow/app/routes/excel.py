from io import BytesIO
from flask import Blueprint, send_file
from openpyxl import Workbook

from app.models.candidate import Candidate

excel_bp = Blueprint("excel", __name__)


@excel_bp.route("/reports/excel")
def export_excel():

    wb = Workbook()

    ws = wb.active

    ws.title = "Candidates"

    ws.append([
        "ID",
        "Name",
        "Email",
        "Phone",
        "LinkedIn",
        "GitHub",
        "Status"
    ])

    candidates = Candidate.query.all()

    for c in candidates:

        ws.append([
            c.candidate_id,
            c.full_name,
            c.email,
            c.phone,
            c.linkedin,
            c.github,
            c.status
        ])

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    return send_file(
        output,
        download_name="Candidate_Report.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )