from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash
)

from app.services.notification_service import NotificationService

notification_bp = Blueprint(
    "notification",
    __name__
)


@notification_bp.route("/notifications")
def notifications():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    notifications = NotificationService.get_all()

    unread_count = NotificationService.unread_count()

    return render_template(
        "notifications.html",
        notifications=notifications,
        unread_count=unread_count
    )


@notification_bp.route("/notifications/read/<int:notification_id>")
def mark_read(notification_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    NotificationService.mark_read(notification_id)

    flash(
        "Notification marked as read.",
        "success"
    )

    return redirect(
        url_for("notification.notifications")
    )


@notification_bp.route("/notifications/read-all")
def mark_all_read():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    NotificationService.mark_all_read()

    flash(
        "All notifications marked as read.",
        "success"
    )

    return redirect(
        url_for("notification.notifications")
    )


@notification_bp.route("/notifications/delete/<int:notification_id>")
def delete_notification(notification_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    NotificationService.delete(notification_id)

    flash(
        "Notification deleted.",
        "success"
    )

    return redirect(
        url_for("notification.notifications")
    )


@notification_bp.route("/notifications/delete-all")
def delete_all_notifications():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    NotificationService.delete_all()

    flash(
        "All notifications deleted.",
        "success"
    )

    return redirect(
        url_for("notification.notifications")
    )