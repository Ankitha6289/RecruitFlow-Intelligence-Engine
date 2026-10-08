from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app.services.settings_service import SettingsService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService

settings_bp = Blueprint(
    "settings",
    __name__
)


# =====================================================
# View & Update Settings
# =====================================================

@settings_bp.route(
    "/admin/settings",
    methods=["GET", "POST"]
)
def settings():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        SettingsService.update(request.form)

        # Activity Log
        ActivityLogService.create(

            session["user_id"],

            "Updated System Settings",

            "Settings"

        )

        # Notification
        NotificationService.create(

            title="Settings Updated",

            message="System settings updated successfully.",

            notification_type="Settings",

            recipient_role="Admin"

        )

        flash(

            "Settings Updated Successfully.",

            "success"

        )

        return redirect(
            url_for("settings.settings")
        )

    settings = SettingsService.get()

    return render_template(

        "settings.html",

        settings=settings

    )