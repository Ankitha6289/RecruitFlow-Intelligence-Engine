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
from app.models.job import Job

from app.services.ai_interview_service import AIInterviewService

ai_interview_bp = Blueprint(
    "ai_interview",
    __name__
)


@ai_interview_bp.route("/admin/ai-interviews")
def interviews():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    interviews = AIInterviewService.get_all()

    return render_template(
        "ai_interviews.html",
        interviews=interviews
    )


@ai_interview_bp.route("/admin/ai-interviews/preview/<int:interview_id>")
def preview_interview(interview_id):
    """Admin preview of an AI interview — bypasses candidate session check."""

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    from app.database.db import db
    from app.models.ai_interview import AIInterview

    ai_interview = db.session.get(AIInterview, interview_id)

    if ai_interview is None:
        flash("AI Interview not found.", "danger")
        return redirect(url_for("ai_interview.interviews"))

    candidate = ai_interview.candidate
    job = ai_interview.job

    questions_payload = AIInterviewService.generate_for_interview(candidate, job)

    return render_template(
        "admin_ai_interview.html",
        interview=ai_interview,
        questions=questions_payload,
        candidate=candidate,
        admin_preview=True
    )



@ai_interview_bp.route(
    "/admin/ai-interviews/add",
    methods=["GET", "POST"]
)
def add_interview():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        scheduled_date = request.form.get("scheduled_date")
        scheduled_time = request.form.get("scheduled_time")

        AIInterviewService.create(

            request.form["candidate_id"],

            request.form["job_id"],
            scheduled_date=scheduled_date if scheduled_date else None,
            scheduled_time=scheduled_time if scheduled_time else None

        )

        flash(

            "AI Interview Scheduled Successfully",

            "success"

        )

        return redirect(

            url_for("ai_interview.interviews")

        )

    candidates = Candidate.query.all()

    jobs = Job.query.all()

    return render_template(
        "add_ai_interview.html",
        candidates=candidates,
        jobs=jobs
    )