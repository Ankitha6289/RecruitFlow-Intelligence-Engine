from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session
)

from app.services.recruiter_dashboard_service import RecruiterDashboardService

recruiter_dashboard_bp = Blueprint(
    "recruiter_dashboard",
    __name__
)


@recruiter_dashboard_bp.route("/recruiter/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    data = RecruiterDashboardService.get_dashboard()

    return render_template(
        "recruiter_dashboard.html",
        data=data
    )