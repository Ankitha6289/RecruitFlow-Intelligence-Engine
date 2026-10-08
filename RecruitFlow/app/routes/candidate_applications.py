from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session
)

from app.models.application import Application

candidate_application_bp = Blueprint(
    "candidate_application",
    __name__
)


@candidate_application_bp.route(
    "/candidate/applications"
)
def my_applications():

    if "candidate_id" not in session:
        return redirect(
            url_for("candidate_auth.login")
        )

    applications = Application.query.filter_by(
        candidate_id=session["candidate_id"]
    ).all()

    return render_template(
        "candidates/my_applications.html",
        applications=applications
    )