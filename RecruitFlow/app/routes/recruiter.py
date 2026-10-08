from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app.services.recruiter_service import RecruiterService

recruiter_bp = Blueprint("recruiter", __name__)


# ---------------------------------------
# View All Recruiters
# ---------------------------------------

@recruiter_bp.route("/recruiters")
def recruiters():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        flash("Access Denied", "danger")
        return redirect(url_for("auth.login"))

    recruiters = RecruiterService.get_all_recruiters()

    return render_template(
        "recruiters.html",
        recruiters=recruiters
    )


# ---------------------------------------
# Add Recruiter
# ---------------------------------------

@recruiter_bp.route("/recruiters/add", methods=["GET", "POST"])
def add_recruiter():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        flash("Access Denied", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        success = RecruiterService.add_recruiter(
            username,
            email,
            password
        )

        if success:

            flash(
                "Recruiter Added Successfully",
                "success"
            )

            return redirect(
                url_for("recruiter.recruiters")
            )

        flash(
            "Email already exists.",
            "danger"
        )

    return render_template(
        "add_recruiter.html"
    )


# ---------------------------------------
# Edit Recruiter
# ---------------------------------------

@recruiter_bp.route(
    "/recruiters/edit/<int:user_id>",
    methods=["GET", "POST"]
)
def edit_recruiter(user_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        flash("Access Denied", "danger")
        return redirect(url_for("auth.login"))

    recruiter = RecruiterService.get_recruiter(
        user_id
    )

    if recruiter is None:

        flash(
            "Recruiter Not Found",
            "danger"
        )

        return redirect(
            url_for("recruiter.recruiters")
        )

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        RecruiterService.update_recruiter(
            user_id,
            username,
            email,
            password
        )

        flash(
            "Recruiter Updated Successfully",
            "success"
        )

        return redirect(
            url_for("recruiter.recruiters")
        )

    return render_template(
        "edit_recruiter.html",
        recruiter=recruiter
    )


# ---------------------------------------
# Delete Recruiter
# ---------------------------------------

@recruiter_bp.route(
    "/recruiters/delete/<int:user_id>"
)
def delete_recruiter(user_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        flash("Access Denied", "danger")
        return redirect(url_for("auth.login"))

    success = RecruiterService.delete_recruiter(
        user_id
    )

    if success:

        flash(
            "Recruiter Deleted Successfully",
            "success"
        )

    else:

        flash(
            "Unable to Delete Recruiter",
            "danger"
        )

    return redirect(
        url_for("recruiter.recruiters")
    )