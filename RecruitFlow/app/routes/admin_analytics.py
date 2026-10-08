from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session
)

from app.services.admin_analytics_service import AdminAnalyticsService

admin_analytics_bp = Blueprint(
    "admin_analytics",
    __name__
)


@admin_analytics_bp.route("/admin/analytics")
def analytics():

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    data = AdminAnalyticsService.get_dashboard()

    return render_template(
        "admin_analytics.html",
        data=data,
        stats=data,
        **data
    )