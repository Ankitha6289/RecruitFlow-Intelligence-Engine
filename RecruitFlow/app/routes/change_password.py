from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app.services.change_password_service import ChangePasswordService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService

change_password_bp = Blueprint(
    "change_password",
    __name__
)


# =====================================================
# Change Password
# =====================================================

@change_password_bp.route(
    "/change-password",
    methods=["GET", "POST"]
)
def change_password():

    # -----------------------------
    # Admin / Recruiter
    # -----------------------------
    if "user_id" in session:

        if request.method == "POST":

            old_password = request.form["old_password"]
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]

            if new_password != confirm_password:

                flash(
                    "New passwords do not match.",
                    "danger"
                )

                return redirect(
                    url_for("change_password.change_password")
                )

            if len(new_password) < 8:

                flash(
                    "Password must contain at least 8 characters.",
                    "danger"
                )

                return redirect(
                    url_for("change_password.change_password")
                )

            success, message = ChangePasswordService.change_user_password(

                session["user_id"],

                old_password,

                new_password

            )

            if success:

                ActivityLogService.create(

                    session["user_id"],

                    "Changed Password",

                    "Authentication"

                )

                NotificationService.create(

                    title="Password Changed",

                    message="Password changed successfully.",

                    notification_type="Security",

                    recipient_role=session.get("role", "User")

                )

                flash(

                    message,

                    "success"

                )

            else:

                flash(

                    message,

                    "danger"

                )

            return redirect(
                url_for("change_password.change_password")
            )

        return render_template(
            "change_password.html"
        )

    # -----------------------------
    # Candidate
    # -----------------------------
    elif "candidate_id" in session:

        if request.method == "POST":

            old_password = request.form["old_password"]
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]

            if new_password != confirm_password:

                flash(
                    "New passwords do not match.",
                    "danger"
                )

                return redirect(
                    url_for("change_password.change_password")
                )

            if len(new_password) < 8:

                flash(
                    "Password must contain at least 8 characters.",
                    "danger"
                )

                return redirect(
                    url_for("change_password.change_password")
                )

            success, message = ChangePasswordService.change_candidate_password(

                session["candidate_id"],

                old_password,

                new_password

            )

            if success:

                ActivityLogService.create(

                    None,

                    "Candidate Changed Password",

                    "Authentication"

                )

                NotificationService.create(

                    title="Password Changed",

                    message="Password changed successfully.",

                    notification_type="Security",

                    recipient_role="Candidate"

                )

                flash(

                    message,

                    "success"

                )

            else:

                flash(

                    message,

                    "danger"

                )

            return redirect(
                url_for("change_password.change_password")
            )

        return render_template(
            "change_password.html"
        )

    return redirect(
        url_for("auth.login")
    )