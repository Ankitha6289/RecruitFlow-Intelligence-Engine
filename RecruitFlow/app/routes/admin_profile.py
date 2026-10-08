from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app.services.admin_profile_service import AdminProfileService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService

admin_profile_bp = Blueprint(
    "admin_profile",
    __name__
)


# ======================================================
# View / Edit Admin Profile
# ======================================================

@admin_profile_bp.route(
    "/admin/profile",
    methods=["GET", "POST"]
)
def profile():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    profile = AdminProfileService.get_profile(
        session["user_id"]
    )

    if profile is None:

        flash(
            "Profile not found.",
            "danger"
        )

        return redirect(
            url_for("auth.admin_dashboard")
        )

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]

        AdminProfileService.update_profile(

            session["user_id"],

            username,

            email

        )

        # ----------------------------------
        # Activity Log
        # ----------------------------------

        ActivityLogService.create(

            session["user_id"],

            "Updated Admin Profile",

            "Admin Profile"

        )

        # ----------------------------------
        # Notification
        # ----------------------------------

        NotificationService.create(

            title="Profile Updated",

            message="Admin profile updated successfully.",

            notification_type="Profile",

            recipient_role="Admin"

        )

        flash(

            "Profile Updated Successfully.",

            "success"

        )

        return redirect(
            url_for("admin_profile.profile")
        )

    return render_template(
        "admin_profile.html",
        profile=profile,
        admin=profile
    )