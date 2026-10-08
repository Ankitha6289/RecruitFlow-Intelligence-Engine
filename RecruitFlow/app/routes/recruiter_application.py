from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash
)

from app.services.recruiter_application_service import RecruiterApplicationService

recruiter_application_bp = Blueprint(
    "recruiter_application",
    __name__
)


@recruiter_application_bp.route("/recruiter/applications")
def applications():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    applications = RecruiterApplicationService.get_all()

    return render_template(
        "recruiter_applications.html",
        applications=applications
    )


@recruiter_application_bp.route(
    "/recruiter/application/shortlist/<int:application_id>"
)
def shortlist(application_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    RecruiterApplicationService.shortlist(application_id)

    flash(
        "Candidate Shortlisted Successfully.",
        "success"
    )

    return redirect(
        url_for("recruiter_application.applications")
    )


@recruiter_application_bp.route(
    "/recruiter/application/reject/<int:application_id>"
)
def reject(application_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    RecruiterApplicationService.reject(application_id)

    flash(
        "Candidate Rejected Successfully.",
        "warning"
    )

    return redirect(
        url_for("recruiter_application.applications")
    )