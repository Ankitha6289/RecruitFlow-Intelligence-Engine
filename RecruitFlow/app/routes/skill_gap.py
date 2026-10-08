from flask import Blueprint, render_template, request

from app.models.candidate import Candidate
from app.models.job import Job
from app.services.skill_gap_service import SkillGapService

skill_gap_bp = Blueprint(
    "skill_gap",
    __name__
)


@skill_gap_bp.route("/skill-gap", methods=["GET", "POST"])
def skill_gap():

    candidates = Candidate.query.all()
    jobs = Job.query.all()

    report = None

    if request.method == "POST":

        candidate_id = int(request.form["candidate_id"])
        job_id = int(request.form["job_id"])

        report = SkillGapService.analyze(
            candidate_id,
            job_id
        )

    return render_template(
        "skill_gap.html",
        candidates=candidates,
        jobs=jobs,
        report=report
    )