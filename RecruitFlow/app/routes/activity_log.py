from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash
)

from app.services.activity_log_service import ActivityLogService

activity_log_bp = Blueprint(
    "activity_log",
    __name__
)


# ---------------------------------------
# View Activity Logs
# ---------------------------------------

@activity_log_bp.route("/activity-logs")
def activity_logs():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    logs = ActivityLogService.get_all()

    return render_template(
        "activity_logs.html",
        logs=logs
    )


# ---------------------------------------
# Delete Single Log
# ---------------------------------------

@activity_log_bp.route("/activity-logs/delete/<int:log_id>")
def delete_log(log_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    ActivityLogService.delete(log_id)

    flash(
        "Activity Log Deleted Successfully",
        "success"
    )

    return redirect(
        url_for("activity_log.activity_logs")
    )


# ---------------------------------------
# Delete All Logs
# ---------------------------------------

@activity_log_bp.route("/activity-logs/delete-all")
def delete_all_logs():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    ActivityLogService.delete_all()

    flash(
        "All Activity Logs Deleted Successfully",
        "success"
    )

    return redirect(
        url_for("activity_log.activity_logs")
    )