from flask import Blueprint, render_template, session, redirect, url_for

from app.services.dashboard_service import DashboardService

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    # User must be logged in
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    data = DashboardService.get_dashboard_data()

    return render_template(
        "dashboard.html",
        data=data
    )