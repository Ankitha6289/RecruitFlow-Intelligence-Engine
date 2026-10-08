from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from app.database.db import db
from app.models.job import Job
from app.models.application import Application

candidate_jobs_bp = Blueprint(
    "candidate_jobs",
    __name__
)


@candidate_jobs_bp.route("/candidate/jobs")
def jobs():

    if "candidate_id" not in session:
        return redirect(
            url_for("candidate_auth.login")
        )

    keyword = request.args.get(
        "keyword",
        ""
    )

    if keyword:

        jobs = Job.query.filter(

            Job.title.ilike(f"%{keyword}%")

        ).all()

    else:

        jobs = Job.query.all()

    return render_template(

        "candidates/jobs.html",

        jobs=jobs,

        keyword=keyword

    )


@candidate_jobs_bp.route("/candidate/jobs/apply/<int:job_id>")
def apply(job_id):

    if "candidate_id" not in session:
        return redirect(
            url_for("candidate_auth.login")
        )

    candidate_id = session["candidate_id"]

    already = Application.query.filter_by(

        candidate_id=candidate_id,

        job_id=job_id

    ).first()

    if already:

        flash(
            "You have already applied for this job.",
            "warning"
        )

        return redirect(
            url_for("candidate_jobs.jobs")
        )

    application = Application(

        candidate_id=candidate_id,

        job_id=job_id,

        status="Applied"

    )

    db.session.add(application)

    db.session.commit()

    flash(
        "Application submitted successfully.",
        "success"
    )

    return redirect(
        url_for("candidate_jobs.jobs")
    )