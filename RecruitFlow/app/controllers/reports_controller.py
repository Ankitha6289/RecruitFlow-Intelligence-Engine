from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

from app.services.reports_service import ReportsService


reports_bp = Blueprint(
    "reports",
    __name__
)


@reports_bp.route("/admin/reports")
def reports_dashboard():

    # Admin Login Check
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    data = ReportsService.get_dashboard_data()

    return render_template(
        "reports/reports_dashboard.html",
        data=data
    )