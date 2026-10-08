from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)

from app.services.interview_management_service import InterviewManagementService
from app.services.job_matching_service import JobMatchingService
from app.models.candidate import Candidate
from app.models.job import Job
from app.services.zoom_meeting_service import ZoomMeetingError

interview_management_bp = Blueprint(
    "interview_management",
    __name__
)


# ==========================================
# View Interviews
# ==========================================

@interview_management_bp.route("/admin/interviews")
def interviews():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "")
    status = request.args.get("status", "")

    interviews = InterviewManagementService.get_all(
        search,
        status
    )

    return render_template(
        "interviews/interviews.html",
        interviews=interviews,
        search=search,
        status=status
    )


# ==========================================
# Add Interview
# ==========================================

@interview_management_bp.route(
    "/admin/interviews/add",
    methods=["GET", "POST"]
)
def add_interview():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        try:
            interview = InterviewManagementService.add(

            request.form["candidate_id"],

            request.form["job_id"],

            request.form["interview_date"],

            request.form["interview_time"],

            request.form["interview_mode"],

            request.form["interviewer"],

            request.form["meeting_link"]

            )
        except ZoomMeetingError as error:
            flash(str(error), "danger")
            return redirect(url_for("interview_management.add_interview"))

        if interview is None:
            flash("Select a valid candidate and job.", "danger")
            return redirect(url_for("interview_management.add_interview"))

        flash(
            "Interview Scheduled Successfully.",
            "success"
        )

        return redirect(
            url_for("interview_management.interviews")
        )

    candidates = Candidate.query.all()

    jobs = Job.query.all()

    return render_template(
        "interviews/add_interview.html",
        candidates=candidates,
        jobs=jobs
    )


# ==========================================
# Interview Details
# ==========================================

@interview_management_bp.route(
    "/admin/interviews/<int:interview_id>"
)
def interview_details(interview_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    interview = InterviewManagementService.get(interview_id)

    if interview is None:

        flash(
            "Interview Not Found.",
            "danger"
        )

        return redirect(
            url_for("interview_management.interviews")
        )

    return render_template(
        "interviews/interview_details.html",
        interview=interview
    )


# ==========================================
# Edit Interview
# ==========================================

@interview_management_bp.route(
    "/admin/interviews/edit/<int:interview_id>",
    methods=["GET", "POST"]
)
def edit_interview(interview_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    interview = InterviewManagementService.get(interview_id)

    if interview is None:

        flash(
            "Interview Not Found.",
            "danger"
        )

        return redirect(
            url_for("interview_management.interviews")
        )

    if request.method == "POST":

        try:
            InterviewManagementService.update(

            interview_id,

            request.form["interview_date"],

            request.form["interview_time"],

            request.form["interview_mode"],

            request.form["interviewer"],

            request.form["meeting_link"],

            request.form["status"]

            )
        except ZoomMeetingError as error:
            flash(str(error), "danger")
            return redirect(url_for("interview_management.edit_interview", interview_id=interview_id))

        flash(
            "Interview Updated Successfully.",
            "success"
        )

        return redirect(
            url_for("interview_management.interviews")
        )

    return render_template(
        "interviews/edit_interview.html",
        interview=interview
    )


# ==========================================
# Update Status (set explicit status value)
# ==========================================

@interview_management_bp.route(
    "/admin/interviews/update-status/<int:interview_id>/<status>"
)
def update_status(interview_id, status):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    InterviewManagementService.update_status(interview_id, status)

    flash(
        f"Interview marked as {status}.",
        "success"
    )

    return redirect(
        url_for("interview_management.interviews")
    )


# ==========================================
# Toggle Status
# ==========================================

@interview_management_bp.route(
    "/admin/interviews/toggle/<int:interview_id>"
)
def toggle_status(interview_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    InterviewManagementService.toggle_status(interview_id)

    flash(
        "Interview Status Updated.",
        "success"
    )

    return redirect(
        url_for("interview_management.interviews")
    )


# ==========================================
# Delete Interview
# ==========================================

@interview_management_bp.route(
    "/admin/interviews/delete/<int:interview_id>"
)
def delete_interview(interview_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    InterviewManagementService.delete(interview_id)

    flash(
        "Interview Deleted Successfully.",
        "success"
    )

    return redirect(
        url_for("interview_management.interviews")
    )


# ==========================================
# Get Best Matching Job for Candidate
# ==========================================

@interview_management_bp.route("/admin/interviews/best-job/<int:candidate_id>")
def get_best_matching_job(candidate_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    best_match = JobMatchingService.get_best_matching_job(candidate_id)

    if best_match and best_match["job"]:
        return jsonify({
            "success": True,
            "job_id": best_match["job"].job_id,
            "job_title": best_match["job"].title,
            "match_score": best_match["score"],
            "matched_skills": best_match["matched_skills"]
        })
    else:
        return jsonify({
            "success": False,
            "message": "No matching job found"
        })