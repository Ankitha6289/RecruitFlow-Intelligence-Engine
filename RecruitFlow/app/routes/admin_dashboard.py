from flask import Blueprint, render_template, session, redirect, url_for

from app.services.admin_dashboard_service import AdminDashboardService


admin_dashboard_bp = Blueprint(
    "admin_dashboard",
    __name__
)


@admin_dashboard_bp.route("/admin/dashboard")
def admin_dashboard():

    # Login Check
    if "user_id" not in session:
        return redirect(url_for("auth.login"))


    data = AdminDashboardService.get_dashboard_data()

    return render_template(
        "admin_dashboard.html",
        data=data,
        stats=data,
        **data
    )