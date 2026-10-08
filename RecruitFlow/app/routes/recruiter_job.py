from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app.services.recruiter_job_service import RecruiterJobService


recruiter_job_bp = Blueprint(
    "recruiter_job",
    __name__
)


# ==========================================
# View Recruiter's Jobs
# ==========================================

@recruiter_job_bp.route("/recruiter/jobs")
def jobs():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    keyword = request.args.get("keyword", "").strip()

    jobs = RecruiterJobService.get_all(
        session["user_id"],
        keyword
    )

    return render_template(
        "recruiter_jobs.html",
        jobs=jobs,
        keyword=keyword
    )


# ==========================================
# Add Job
# ==========================================

@recruiter_job_bp.route(
    "/recruiter/jobs/add",
    methods=["GET", "POST"]
)
def add_job():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        RecruiterJobService.add(

            session["user_id"],

            request.form.get("title", "").strip(),

            request.form.get("company", "").strip(),

            request.form.get("location", "").strip(),

            request.form.get("experience", "").strip(),

            request.form.get("salary", "").strip(),

            request.form.get("skills", "").strip(),

            request.form.get("description", "").strip()

        )

        flash(
            "Job Added Successfully.",
            "success"
        )

        return redirect(
            url_for("recruiter_job.jobs")
        )

    return render_template(
        "recruiter_add_job.html"
    )


# ==========================================
# Edit Job
# ==========================================

@recruiter_job_bp.route(
    "/recruiter/jobs/edit/<int:job_id>",
    methods=["GET", "POST"]
)
def edit_job(job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    job = RecruiterJobService.get(job_id)

    if job is None:

        flash(
            "Job Not Found.",
            "danger"
        )

        return redirect(
            url_for("recruiter_job.jobs")
        )

    if request.method == "POST":

        RecruiterJobService.update(

            job_id,

            request.form.get("title", "").strip(),

            request.form.get("company", "").strip(),

            request.form.get("location", "").strip(),

            request.form.get("experience", "").strip(),

            request.form.get("salary", "").strip(),

            request.form.get("skills", "").strip(),

            request.form.get("description", "").strip()

        )

        flash(
            "Job Updated Successfully.",
            "success"
        )

        return redirect(
            url_for("recruiter_job.jobs")
        )

    return render_template(
        "recruiter_edit_job.html",
        job=job
    )


# ==========================================
# Delete Job
# ==========================================

@recruiter_job_bp.route(
    "/recruiter/jobs/delete/<int:job_id>"
)
def delete_job(job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    RecruiterJobService.delete(job_id)

    flash(
        "Job Deleted Successfully.",
        "success"
    )

    return redirect(
        url_for("recruiter_job.jobs")
    )


# ==========================================
# Activate / Deactivate Job
# ==========================================

@recruiter_job_bp.route(
    "/recruiter/jobs/toggle/<int:job_id>"
)
def toggle_job(job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    RecruiterJobService.toggle(job_id)

    flash(
        "Job Status Updated.",
        "success"
    )

    return redirect(
        url_for("recruiter_job.jobs")
    )