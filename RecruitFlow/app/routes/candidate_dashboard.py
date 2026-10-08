from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash
)

from app.services.candidate_dashboard_service import CandidateDashboardService

candidate_dashboard_bp = Blueprint(
    "candidate_dashboard",
    __name__
)


@candidate_dashboard_bp.route("/candidate/dashboard")
def dashboard():

    if "candidate_id" not in session:
        return redirect(url_for("candidate_auth.login"))

    data = CandidateDashboardService.get_dashboard(
        session["candidate_id"]
    )

    if data["candidate"] is None:

        session.clear()

        flash(
            "Candidate not found. Please login again.",
            "danger"
        )

        return redirect(
            url_for("candidate_auth.login")
        )

    return render_template(
        "candidates/dashboard.html",
        **data
    )