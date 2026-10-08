from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from app.database.db import db
from app.models.candidate import Candidate

candidate_settings_bp = Blueprint(
    "candidate_settings",
    __name__
)


@candidate_settings_bp.route(
    "/candidate/settings",
    methods=["GET", "POST"]
)
def settings():

    if "candidate_id" not in session:

        return redirect(
            url_for("candidate_auth.login")
        )

    candidate = db.session.get(
        Candidate,
        session["candidate_id"]
    )

    if request.method == "POST":

        current_password = request.form["current_password"]

        new_password = request.form["new_password"]

        confirm_password = request.form["confirm_password"]

        if not check_password_hash(
            candidate.password,
            current_password
        ):

            flash(
                "Current password is incorrect.",
                "danger"
            )

            return redirect(
                url_for("candidate_settings.settings")
            )

        if new_password != confirm_password:

            flash(
                "Passwords do not match.",
                "warning"
            )

            return redirect(
                url_for("candidate_settings.settings")
            )

        candidate.password = generate_password_hash(
            new_password
        )

        db.session.commit()

        flash(
            "Password updated successfully.",
            "success"
        )

        return redirect(
            url_for("candidate_settings.settings")
        )

    return render_template(
        "candidates/settings.html"
    )