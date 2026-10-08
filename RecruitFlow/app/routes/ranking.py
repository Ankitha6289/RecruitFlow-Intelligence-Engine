from flask import Blueprint, render_template, session, redirect, url_for

from app.services.job_service import JobService
from app.services.ranking_service import RankingService

ranking_bp = Blueprint("ranking", __name__)


@ranking_bp.route("/ranking/<int:job_id>")
def ranking(job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    job = JobService.get(job_id)

    rankings = RankingService.rank_candidates(job_id)

    return render_template(
        "ranking.html",
        job=job,
        rankings=rankings
    )