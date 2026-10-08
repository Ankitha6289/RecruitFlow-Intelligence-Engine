from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session
)

from app.models.notification import Notification

candidate_notification_bp = Blueprint(
    "candidate_notification",
    __name__
)


@candidate_notification_bp.route(
    "/candidate/notifications"
)
def notifications():

    if "candidate_id" not in session:

        return redirect(
            url_for("candidate_auth.login")
        )

    notifications = Notification.query.filter_by(
        recipient_role="Candidate"
    ).order_by(
        Notification.created_at.desc()
    ).all()

    return render_template(
        "candidates/notifications.html",
        notifications=notifications
    )