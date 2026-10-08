from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app.models.candidate import Candidate
from app.models.interview import Interview

from app.services.interview_service import InterviewService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService
from app.services.job_matching_service import JobMatchingService

interview_bp = Blueprint(
    "interview",
    __name__
)


# ======================================================
# View Interviews
# ======================================================

@interview_bp.route("/interviews")
def interviews():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    interviews = InterviewService.get_all()

    return render_template(
        "interviews.html",
        interviews=interviews
    )


# ======================================================
# Schedule Interview
# ======================================================

@interview_bp.route(
    "/interviews/add/<int:candidate_id>",
    methods=["GET", "POST"]
)
def schedule_interview(candidate_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    candidate = Candidate.query.get_or_404(candidate_id)

    if request.method == "POST":

        try:
            interview = InterviewService.schedule(
                candidate_id,
                request.form["interviewer"],
                request.form["interview_date"],
                request.form["interview_time"],
                request.form["mode"]
            )
        except Exception as error:
            flash(f"Interview scheduling failed: {error}", "danger")
            return redirect(url_for("interview.schedule_interview", candidate_id=candidate_id))

        if interview is None:
            flash("No suitable job could be matched to this candidate's resume.", "danger")
            return redirect(url_for("interview.schedule_interview", candidate_id=candidate_id))

        # -------------------------
        # Activity Log
        # -------------------------

        ActivityLogService.create(

            session["user_id"],

            "Scheduled Interview",

            "Interview"

        )

        # -------------------------
        # Notification
        # -------------------------

        NotificationService.create(

            title="Interview Scheduled",

            message="Interview has been scheduled.",

            notification_type="Interview",

            recipient_role="Recruiter"

        )

        flash(
            "Interview Scheduled Successfully",
            "success"
        )

        return redirect(
            url_for("interview.interviews")
        )

    best_match = JobMatchingService.get_best_matching_job(candidate_id)
    return render_template(
        "schedule_interview.html",
        candidate=candidate,
        best_match=best_match
    )
# ======================================================
# Edit Interview
# ======================================================

@interview_bp.route(
    "/interviews/edit/<int:interview_id>",
    methods=["GET", "POST"]
)
def edit_interview(interview_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    interview = InterviewService.get(interview_id)

    if interview is None:

        flash(
            "Interview Not Found",
            "danger"
        )

        return redirect(
            url_for("interview.interviews")
        )

    if request.method == "POST":

        try:
            InterviewService.update(
                interview_id,
                request.form["interviewer"],
                request.form["interview_date"],
                request.form["interview_time"],
                request.form["mode"],
                request.form["status"]
            )
        except Exception as error:
            flash(f"Interview update failed: {error}", "danger")
            return redirect(url_for("interview.edit_interview", interview_id=interview_id))

        # ----------------------------------
        # Activity Log
        # ----------------------------------

        ActivityLogService.create(

            session["user_id"],

            "Updated Interview",

            "Interview"

        )

        # ----------------------------------
        # Notification
        # ----------------------------------

        NotificationService.create(

            title="Interview Updated",

            message="Interview details have been updated.",

            notification_type="Interview",

            recipient_role="Recruiter"

        )

        flash(

            "Interview Updated Successfully",

            "success"

        )

        return redirect(
            url_for("interview.interviews")
        )

    return render_template(

        "edit_interview.html",

        interview=interview

    )


@interview_bp.route(
    "/meeting/<int:interview_id>"
)
def meeting_room(interview_id):

    interview = Interview.query.get_or_404(interview_id)

    if "candidate_id" not in session and "user_id" not in session:
        return redirect(url_for("candidate_auth.login"))

    return render_template(
        "meeting_room.html",
        interview=interview
    )


# ======================================================
# Delete Interview
# ======================================================

@interview_bp.route(
    "/interviews/delete/<int:interview_id>"
)
def delete_interview(interview_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    interview = InterviewService.get(interview_id)

    if interview is None:

        flash(
            "Interview Not Found",
            "danger"
        )

        return redirect(
            url_for("interview.interviews")
        )

    InterviewService.delete(interview_id)

    # ----------------------------------
    # Activity Log
    # ----------------------------------

    ActivityLogService.create(

        session["user_id"],

        "Deleted Interview",

        "Interview"

    )

    # ----------------------------------
    # Notification
    # ----------------------------------

    NotificationService.create(

        title="Interview Deleted",

        message="An interview has been deleted.",

        notification_type="Interview",

        recipient_role="Recruiter"

    )

    flash(

        "Interview Deleted Successfully",

        "success"

    )

    return redirect(
        url_for("interview.interviews")
    )