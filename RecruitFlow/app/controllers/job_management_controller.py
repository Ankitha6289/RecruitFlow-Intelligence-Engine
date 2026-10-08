from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from app.services.job_management_service import JobManagementService

job_management_bp = Blueprint(
    "job_management",
    __name__
)


# ===================================================
# Job List
# ===================================================

@job_management_bp.route("/admin/jobs")
def jobs():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "")
    status = request.args.get("status", "")

    jobs = JobManagementService.get_all(
        search,
        status
    )

    return render_template(
        "jobs/jobs.html",
        jobs=jobs,
        search=search,
        status=status
    )


# ===================================================
# Add Job
# ===================================================

@job_management_bp.route(
    "/admin/jobs/add",
    methods=["GET", "POST"]
)
def add_job():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        JobManagementService.add(

            request.form["title"],
            request.form["company"],
            request.form["location"],
            request.form["salary"],
            request.form["experience"],
            request.form["skills"],
            request.form["description"]

        )

        flash(
            "Job Added Successfully.",
            "success"
        )

        return redirect(
            url_for("job_management.jobs")
        )

    return render_template(
        "jobs/add_job.html"
    )


# ===================================================
# View Job
# ===================================================

@job_management_bp.route(
    "/admin/jobs/<int:job_id>"
)
def job_details(job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    job = JobManagementService.get(job_id)

    if not job:

        flash(
            "Job Not Found.",
            "danger"
        )

        return redirect(
            url_for("job_management.jobs")
        )

    return render_template(
        "jobs/job_details.html",
        job=job
    )


# ===================================================
# Edit Job
# ===================================================

@job_management_bp.route(
    "/admin/jobs/edit/<int:job_id>",
    methods=["GET", "POST"]
)
def edit_job(job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    job = JobManagementService.get(job_id)

    if not job:

        flash(
            "Job Not Found.",
            "danger"
        )

        return redirect(
            url_for("job_management.jobs")
        )

    if request.method == "POST":

        JobManagementService.update(

            job_id,

            request.form["title"],
            request.form["company"],
            request.form["location"],
            request.form["salary"],
            request.form["experience"],
            request.form["skills"],
            request.form["description"]

        )

        flash(
            "Job Updated Successfully.",
            "success"
        )

        return redirect(
            url_for("job_management.jobs")
        )

    return render_template(
        "jobs/edit_job.html",
        job=job
    )


# ===================================================
# Delete Job
# ===================================================

@job_management_bp.route(
    "/admin/jobs/delete/<int:job_id>"
)
def delete_job(job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    JobManagementService.delete(job_id)

    flash(
        "Job Deleted Successfully.",
        "success"
    )

    return redirect(
        url_for("job_management.jobs")
    )


# ===================================================
# Toggle Status
# ===================================================

@job_management_bp.route(
    "/admin/jobs/toggle/<int:job_id>"
)
def toggle_job(job_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    JobManagementService.toggle_status(job_id)

    flash(
        "Job Status Updated Successfully.",
        "success"
    )

    return redirect(
        url_for("job_management.jobs")
    )


# ===================================================
# Export PDF
# ===================================================

@job_management_bp.route(
    "/admin/jobs/export/pdf"
)
def export_pdf():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return JobManagementService.export_pdf()


# ===================================================
# Export Excel
# ===================================================

@job_management_bp.route(
    "/admin/jobs/export/excel"
)
def export_excel():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return JobManagementService.export_excel()