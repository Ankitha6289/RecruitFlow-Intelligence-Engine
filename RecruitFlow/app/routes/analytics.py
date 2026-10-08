from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash
)

from app.services.analytics_service import AnalyticsService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService

analytics_bp = Blueprint(
    "analytics",
    __name__
)


# ======================================================
# Analytics Dashboard
# ======================================================

@analytics_bp.route("/analytics")
def analytics_dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    data = AnalyticsService.dashboard()

    # ----------------------------------
    # Activity Log
    # ----------------------------------

    ActivityLogService.create(

        session["user_id"],

        "Viewed Analytics Dashboard",

        "Analytics"

    )

    # ----------------------------------
    # Notification
    # ----------------------------------

    NotificationService.create(

        title="Analytics Dashboard",

        message="Analytics dashboard opened.",

        notification_type="Analytics",

        recipient_role="Admin"

    )

    return render_template(

        "analytics_dashboard.html",

        data=data

    )