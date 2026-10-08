from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    session,
    redirect,
    url_for,
    flash
)

from app.models.candidate import Candidate
from app.models.job import Job
from app.services.job_matching_service import JobMatchingService

match_bp = Blueprint(
    "match",
    __name__
)


# =====================================
# Job Matching Home Page
# =====================================

@match_bp.route("/job-matching")
def job_matching():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    candidates = Candidate.query.all()
    jobs = Job.query.all()

    return render_template(
        "job_matching.html",
        candidates=candidates,
        jobs=jobs
    )


@match_bp.route("/job-matching/best-job")
def best_matching_job():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    candidate_id = request.args.get("candidate_id", type=int)
    if candidate_id is None:
        return jsonify({"error": "Candidate ID is required."}), 400

    best_match = JobMatchingService.get_best_matching_job(candidate_id)
    if not best_match:
        return jsonify({"job_id": None, "score": None})

    job = best_match["job"]
    return jsonify(
        {
            "job_id": job.job_id,
            "title": job.title,
            "company": job.company,
            "score": best_match["score"],
        }
    )


# =====================================
# Calculate Match
# =====================================

@match_bp.route("/match/<int:candidate_id>/<int:job_id>")
def match(candidate_id, job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    result = JobMatchingService.calculate_match(
        candidate_id,
        job_id
    )

    if result is None:

        flash(
            "Candidate or Job not found.",
            "danger"
        )

        return redirect(
            url_for("match.job_matching")
        )

    flash(
        "Job Matching Completed Successfully.",
        "success"
    )

    return render_template(
        "job_match.html",
        candidate=result["candidate"],
        job=result["job"],
        result=result
    )