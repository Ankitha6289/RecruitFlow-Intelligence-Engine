from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from app.models.application import Application
from app.services.recruiter_interview_service import RecruiterInterviewService
from app.services.job_matching_service import JobMatchingService
from app.services.zoom_meeting_service import ZoomMeetingError

recruiter_interview_bp = Blueprint(
    "recruiter_interview",
    __name__
)


@recruiter_interview_bp.route(
    "/interviews/add/<int:application_id>",
    methods=["GET", "POST"]
)
def add_interview(application_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    application = Application.query.get_or_404(application_id)

    if request.method == "POST":

        try:
            interview = RecruiterInterviewService.create(

            application_id,

            request.form["interviewer"],

            request.form["interview_date"],

            request.form["interview_time"],

            request.form["mode"]

            )
        except ZoomMeetingError as error:
            flash(str(error), "danger")
            return redirect(url_for("recruiter_interview.add_interview", application_id=application_id))

        if interview is None:
            flash("Could not schedule an interview for this application.", "danger")
            return redirect(url_for("recruiter_application.applications"))

        flash(
            "Interview Scheduled Successfully.",
            "success"
        )

        return redirect(
            url_for("recruiter_application.applications")
        )

    best_match = JobMatchingService.get_best_matching_job(application.candidate_id)
    recommended_job = best_match["job"] if best_match else application.job

    return render_template(

        "recruiter_add_interview.html",

        application=application,
        best_match=best_match,
        recommended_job=recommended_job,

    )