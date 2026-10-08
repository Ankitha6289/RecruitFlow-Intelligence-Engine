from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    request,
    flash,
    jsonify,
    current_app,
    send_from_directory,
    abort,
)
import os
import uuid

from app.database.db import db
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.models.interview_proctor_event import InterviewProctorEvent
from app.services.ai_interview_service import AIInterviewService

candidate_interview_bp = Blueprint(
    "candidate_interview",
    __name__
)


@candidate_interview_bp.route(
    "/candidate/interviews"
)
def interviews():

    if "candidate_id" not in session:

        return redirect(
            url_for("candidate_auth.login")
        )

    interviews = Interview.query.filter_by(
        candidate_id=session["candidate_id"]
    ).order_by(
        Interview.interview_date.desc(),
        Interview.interview_time.desc()
    ).all()

    return render_template(
        "candidates/interviews.html",
        interviews=interviews
    )


@candidate_interview_bp.route("/candidate/questions")
def questions():

    if "candidate_id" not in session:
        return redirect(url_for("candidate_auth.login"))

    interview_id = request.args.get("interview_id", type=int)

    interview = None
    if interview_id:
        interview = Interview.query.filter_by(
            candidate_id=session["candidate_id"],
            interview_id=interview_id
        ).first()

    if interview is None:
        interview = Interview.query.filter_by(
            candidate_id=session["candidate_id"]
        ).order_by(
            Interview.interview_date.desc(),
            Interview.interview_time.desc()
        ).first()

    if interview is None:
        flash("No interview is available yet. Please wait for a recruiter to schedule one.", "info")
        return redirect(url_for("candidate_interview.interviews"))

    candidate = db.session.get(Candidate, session["candidate_id"])
    questions_payload = AIInterviewService.generate_for_interview(candidate, interview.job)

    return render_template(
        "candidates/ai_interview.html",
        interview=interview,
        questions=questions_payload,
        candidate=candidate
    )


@candidate_interview_bp.route("/candidate/interview-proctor-event", methods=["POST"])
def save_proctor_event():

    if "candidate_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    interview_id = data.get("interview_id")
    event_type = data.get("event_type")
    details = data.get("details", "")
    severity = data.get("severity", "low")

    if not interview_id or not event_type:
        return jsonify({"error": "interview_id and event_type are required"}), 400

    interview = db.session.get(Interview, interview_id)
    if interview is None or interview.candidate_id != session["candidate_id"]:
        return jsonify({"error": "Unauthorized interview access"}), 403

    event = InterviewProctorEvent(
        interview_id=interview_id,
        event_type=event_type,
        details=details,
        severity=severity
    )
    db.session.add(event)
    db.session.commit()

    return jsonify({"success": True, "event_id": event.event_id})


@candidate_interview_bp.route("/candidate/interview-evaluate", methods=["POST"])
def evaluate_interview_answer():

    if "candidate_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    interview_id = data.get("interview_id")
    question = data.get("question")
    transcript = data.get("transcript", "")

    if not interview_id or not question:
        return jsonify({"error": "interview_id and question are required"}), 400

    interview = db.session.get(Interview, interview_id)
    if interview is None or interview.candidate_id != session["candidate_id"]:
        return jsonify({"error": "Unauthorized interview access"}), 403

    candidate = db.session.get(Candidate, session["candidate_id"])
    evaluation = AIInterviewService.evaluate_answer(candidate, interview.job, question, transcript)

    return jsonify({"success": True, "evaluation": evaluation})


@candidate_interview_bp.route("/candidate/interview-complete", methods=["POST"])
def complete_interview():

    if "candidate_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    interview_id = request.form.get("interview_id", type=int)
    transcript = request.form.get("transcript", "").strip()
    duration_seconds = request.form.get("duration_seconds", default=0, type=int)
    recording = request.files.get("recording")

    if not interview_id or not transcript or not recording:
        return jsonify({"error": "Interview ID, transcript, and recording are required."}), 400

    interview = db.session.get(Interview, interview_id)
    if interview is None or interview.candidate_id != session["candidate_id"]:
        return jsonify({"error": "Unauthorized interview access"}), 403

    if interview.status in {"Selected", "Rejected"}:
        return jsonify({"error": "This interview has already been completed."}), 409

    recording.stream.seek(0, os.SEEK_END)
    recording_size = recording.stream.tell()
    recording.stream.seek(0)
    if recording_size == 0 or recording_size > 250 * 1024 * 1024:
        return jsonify({"error": "Recording must be between 1 byte and 250 MB."}), 413

    recording_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "ai_interviews")
    os.makedirs(recording_dir, exist_ok=True)
    filename = f"interview_{interview_id}_{uuid.uuid4().hex}.webm"
    recording.save(os.path.join(recording_dir, filename))
    recording_path = os.path.join("ai_interviews", filename)

    result = AIInterviewService.finalize_candidate_interview(
        interview,
        transcript,
        max(0, duration_seconds),
        recording_path,
    )
    if result is None:
        os.remove(os.path.join(recording_dir, filename))
        return jsonify({"error": "Could not complete this interview."}), 500

    return jsonify({
        "success": True,
        "message": "Interview completed and candidate notified.",
        "status": result["status"],
        "score": result["score"],
    })


@candidate_interview_bp.route("/staff/interviews/<int:interview_id>/ai-recording")
def staff_ai_recording(interview_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    interview = db.session.get(Interview, interview_id)
    if interview is None or not interview.ai_recording_path:
        abort(404)

    filename = os.path.basename(interview.ai_recording_path)
    recording_directory = os.path.join(
        current_app.config["UPLOAD_FOLDER"], "ai_interviews"
    )
    return send_from_directory(
        recording_directory,
        filename,
        mimetype="video/webm",
        as_attachment=False,
        conditional=True,
    )