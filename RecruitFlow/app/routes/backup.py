import os

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    send_file,
    request
)

from app.services.backup_service import BackupService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService

backup_bp = Blueprint(
    "backup",
    __name__
)


# =====================================================
# Backup Dashboard
# =====================================================

@backup_bp.route("/admin/backup")
def backup():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    latest = BackupService.latest_backup()

    return render_template(
        "backup.html",
        latest_backup=latest
    )


# =====================================================
# Create Backup
# =====================================================

@backup_bp.route("/admin/backup/create")
def create_backup():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    backup_file = BackupService.create_backup()

    if backup_file:

        ActivityLogService.create(

            session["user_id"],

            "Database Backup Created",

            "Backup"

        )

        NotificationService.create(

            title="Database Backup",

            message="Database backup created successfully.",

            notification_type="Backup",

            recipient_role="Admin"

        )

        flash(

            "Database Backup Created Successfully.",

            "success"

        )

    else:

        flash(

            "Backup Failed.",

            "danger"

        )

    return redirect(
        url_for("backup.backup")
    )


# =====================================================
# Download Latest Backup
# =====================================================

@backup_bp.route("/admin/backup/download")
def download_backup():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    latest = BackupService.latest_backup()

    if latest is None:

        flash(

            "No Backup Found.",

            "warning"

        )

        return redirect(
            url_for("backup.backup")
        )

    ActivityLogService.create(

        session["user_id"],

        "Downloaded Database Backup",

        "Backup"

    )

    return send_file(

        latest,

        as_attachment=True

    )


# =====================================================
# Restore Backup
# =====================================================

@backup_bp.route(
    "/admin/backup/restore",
    methods=["POST"]
)
def restore_backup():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    latest = BackupService.latest_backup()

    if latest is None:

        flash(

            "No Backup Available.",

            "warning"

        )

        return redirect(
            url_for("backup.backup")
        )

    success = BackupService.restore_backup(latest)

    if success:

        ActivityLogService.create(

            session["user_id"],

            "Database Restored",

            "Backup"

        )

        NotificationService.create(

            title="Database Restore",

            message="Database restored successfully.",

            notification_type="Backup",

            recipient_role="Admin"

        )

        flash(

            "Database Restored Successfully.",

            "success"

        )

    else:

        flash(

            "Restore Failed.",

            "danger"

        )

    return redirect(
        url_for("backup.backup")
    )