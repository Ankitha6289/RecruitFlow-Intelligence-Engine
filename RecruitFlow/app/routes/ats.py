from flask import Blueprint, render_template, redirect, url_for, session

from app.services.ats_service import ATSService

ats_bp = Blueprint("ats", __name__)


@ats_bp.route("/ats/<int:candidate_id>")
def ats(candidate_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    report = ATSService.analyze(candidate_id)

    return render_template(
        "ats_report.html",
        report=report
    )