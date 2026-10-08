from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app.services.recruiter_profile_service import RecruiterProfileService

recruiter_profile_bp = Blueprint(
    "recruiter_profile",
    __name__
)


# -------------------------------------
# Recruiter Profile
# -------------------------------------

@recruiter_profile_bp.route("/recruiter/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = RecruiterProfileService.get_user(
        session["user_id"]
    )

    return render_template(
        "recruiter_profile.html",
        user=user
    )


# -------------------------------------
# Update Profile
# -------------------------------------

@recruiter_profile_bp.route(
    "/recruiter/profile/update",
    methods=["POST"]
)
def update_profile():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    RecruiterProfileService.update_profile(

        session["user_id"],

        request.form["username"],

        request.form["email"]

    )

    flash(
        "Profile Updated Successfully",
        "success"
    )

    return redirect(
        url_for("recruiter_profile.profile")
    )


# -------------------------------------
# Change Password
# -------------------------------------

@recruiter_profile_bp.route(
    "/recruiter/profile/change-password",
    methods=["POST"]
)
def change_password():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    success, message = RecruiterProfileService.change_password(

        session["user_id"],

        request.form["current_password"],

        request.form["new_password"]

    )

    if success:

        flash(message, "success")

    else:

        flash(message, "danger")

    return redirect(
        url_for("recruiter_profile.profile")
    )