from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app.services.job_service import JobService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService

job_bp = Blueprint(
    "job",
    __name__
)


# ======================================================
# View Jobs
# ======================================================

@job_bp.route("/jobs")
def jobs():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    keyword = request.args.get(
        "keyword",
        ""
    ).strip()

    if keyword:

        jobs = JobService.search(keyword)

    else:

        jobs = JobService.get_all()

    return render_template(

        "jobs.html",

        jobs=jobs,

        keyword=keyword

    )


# ======================================================
# Add Job
# ======================================================

@job_bp.route(
    "/jobs/add",
    methods=["GET", "POST"]
)
def add_job():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        JobService.add(request.form)

        # ----------------------------
        # Activity Log
        # ----------------------------

        ActivityLogService.create(

            session["user_id"],

            "Created New Job",

            "Jobs"

        )

        # ----------------------------
        # Notification
        # ----------------------------

        NotificationService.create(

            title="Job Created",

            message="A new job has been added.",

            notification_type="Jobs",

            recipient_role="Recruiter"

        )

        flash(

            "Job Added Successfully",

            "success"

        )

        return redirect(
            url_for("job.jobs")
        )

    return render_template(
        "add_job.html"
    )
# ======================================================
# Edit Job
# ======================================================

@job_bp.route(
    "/jobs/edit/<int:job_id>",
    methods=["GET", "POST"]
)
def edit_job(job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    job = JobService.get(job_id)

    if job is None:

        flash(
            "Job Not Found",
            "danger"
        )

        return redirect(
            url_for("job.jobs")
        )

    if request.method == "POST":

        JobService.update(
            job_id,
            request.form
        )

        # ----------------------------
        # Activity Log
        # ----------------------------

        ActivityLogService.create(

            session["user_id"],

            "Updated Job",

            "Jobs"

        )

        # ----------------------------
        # Notification
        # ----------------------------

        NotificationService.create(

            title="Job Updated",

            message="A job has been updated successfully.",

            notification_type="Jobs",

            recipient_role="Recruiter"

        )

        flash(

            "Job Updated Successfully",

            "success"

        )

        return redirect(
            url_for("job.jobs")
        )

    return render_template(

        "edit_job.html",

        job=job

    )
# ======================================================
# Delete Job
# ======================================================

@job_bp.route("/jobs/delete/<int:job_id>")
def delete_job(job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    job = JobService.get(job_id)

    if job is None:

        flash(
            "Job Not Found",
            "danger"
        )

        return redirect(
            url_for("job.jobs")
        )

    JobService.delete(job_id)

    # ----------------------------------
    # Activity Log
    # ----------------------------------

    ActivityLogService.create(

        session["user_id"],

        "Deleted Job",

        "Jobs"

    )

    # ----------------------------------
    # Notification
    # ----------------------------------

    NotificationService.create(

        title="Job Deleted",

        message="A job has been deleted successfully.",

        notification_type="Jobs",

        recipient_role="Recruiter"

    )

    flash(

        "Job Deleted Successfully",

        "success"

    )

    return redirect(
        url_for("job.jobs")
    )