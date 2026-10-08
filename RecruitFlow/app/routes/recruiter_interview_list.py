from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    request
)

from app.models.interview_proctor_event import InterviewProctorEvent
from app.services.recruiter_interview_list_service import RecruiterInterviewListService

recruiter_interview_list_bp = Blueprint(
    "recruiter_interview_list",
    __name__
)


@recruiter_interview_list_bp.route("/recruiter/interviews")
def interviews():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    risk_filter = request.args.get("risk", "all")
    interviews = RecruiterInterviewListService.get_all()

    if risk_filter != "all":
        interviews = [i for i in interviews if getattr(i, "proctor_risk", "Safe") == risk_filter]

    return render_template(
        "recruiter_interviews.html",
        interviews=interviews,
        risk_filter=risk_filter
    )


@recruiter_interview_list_bp.route(
    "/recruiter/interview/proctor/<int:interview_id>"
)
def proctor_summary(interview_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    interview = RecruiterInterviewListService.get_by_id(interview_id)
    if interview is None:
        flash("Interview not found.", "danger")
        return redirect(url_for("recruiter_interview_list.interviews"))

    events = interview.proctor_events or []
    counts = {}
    severity_score = 0
    weights = {
        "tab_switch":       15,
        "copy_attempt":      5,
        "paste_attempt":     5,
        "cut_attempt":       5,
        "right_click":       5,
        "focus_loss":       10,
        "window_resize":    10,
        "camera_away":      20,
        "multiple_faces":   25,
        "phone_detected":   30,
        "devtools_open":    35,
        "fullscreen_exit":  18,
        "audio_anomaly":    12,
        "screenshot_attempt": 8,
        "eye_contact_loss":  5,
    }

    for event in events:
        counts[event.event_type] = counts.get(event.event_type, 0) + 1
        severity_score += weights.get(event.event_type, 10)

    if severity_score >= 51:
        risk = "High Risk"
    elif severity_score >= 21:
        risk = "Suspicious"
    else:
        risk = "Safe"

    return render_template(
        "recruiter_interview_proctor.html",
        interview=interview,
        events=events,
        counts=counts,
        severity_score=severity_score,
        risk=risk
    )


@recruiter_interview_list_bp.route(
    "/recruiter/interview/complete/<int:interview_id>"
)
def complete(interview_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    RecruiterInterviewListService.complete(interview_id)

    flash(
        "Interview Completed.",
        "success"
    )

    return redirect(
        url_for("recruiter_interview_list.interviews")
    )


@recruiter_interview_list_bp.route(
    "/recruiter/interview/select/<int:interview_id>"
)
def select(interview_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    RecruiterInterviewListService.select(interview_id)

    flash(
        "Candidate Selected.",
        "success"
    )

    return redirect(
        url_for("recruiter_interview_list.interviews")
    )


@recruiter_interview_list_bp.route(
    "/recruiter/interview/reject/<int:interview_id>"
)
def reject(interview_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    RecruiterInterviewListService.reject(interview_id)

    flash(
        "Candidate Rejected.",
        "warning"
    )

    return redirect(
        url_for("recruiter_interview_list.interviews")
    )


@recruiter_interview_list_bp.route(
    "/recruiter/interview/delete/<int:interview_id>"
)
def delete(interview_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    RecruiterInterviewListService.delete(interview_id)

    flash(
        "Interview Deleted.",
        "danger"
    )

    return redirect(
        url_for("recruiter_interview_list.interviews")
    )