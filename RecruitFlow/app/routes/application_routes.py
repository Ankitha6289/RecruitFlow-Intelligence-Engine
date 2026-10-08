from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    request
)

from app.services.application_service import ApplicationService
from app.services.email_service import EmailService
from app.models.application import Application

application_bp = Blueprint(
    "application",
    __name__
)


# =====================================
# Candidate Apply Job
# =====================================

@application_bp.route("/apply/<int:job_id>")
def apply(job_id):

    if "candidate_id" not in session:

        return redirect(url_for("candidate_auth.login"))

    application = ApplicationService.apply(

        session["candidate_id"],

        job_id

    )

    if application:

        flash(

            "Application Submitted Successfully.",

            "success"

        )

    else:

        flash(

            "You have already applied for this job.",

            "warning"

        )

    return redirect(url_for("candidate_dashboard.dashboard"))


# =====================================
# Candidate View Applications
# =====================================

@application_bp.route("/candidate/applications")
def candidate_applications():

    if "candidate_id" not in session:

        return redirect(url_for("candidate_auth.login"))

    applications = ApplicationService.get_candidate_applications(

        session["candidate_id"]

    )

    return render_template(

        "candidates/applications.html",

        applications=applications

    )


# =====================================
# Recruiter View Applications
# =====================================

@application_bp.route("/admin/applications")
def all_applications():

    applications = ApplicationService.get_all()

    return render_template(

        "admin/applications.html",

        applications=applications

    )


# =====================================
# Update Candidate Status
# =====================================

@application_bp.route(

    "/admin/application/update/<int:application_id>",

    methods=["POST"]

)

def update_status(application_id):

    status = request.form["status"]

    remarks = request.form["remarks"]

    application = ApplicationService.update_status(

        application_id,

        status,

        remarks

    )

    if application:

        candidate = application.candidate

        if status == "Selected":
         EmailService.selection_email(candidate)

        elif status == "Rejected":
         EmailService.rejection_email(candidate)

        elif status == "Technical Interview":
         EmailService.interview_email(candidate)

        elif status == "Offer Sent":
         EmailService.offer_email(candidate)

        flash(

            "Application Updated Successfully.",

            "success"

        )

    return redirect(

        url_for("application.all_applications")

    )


# =====================================
# Delete Application
# =====================================

@application_bp.route(

    "/admin/application/delete/<int:application_id>"

)

def delete_application(application_id):

    ApplicationService.delete(application_id)

    flash(

        "Application Deleted.",

        "success"

    )

    return redirect(

        url_for("application.all_applications")

    )