from flask import Blueprint, redirect, url_for, flash, session

from app.services.candidate_status_service import CandidateStatusService

status_bp = Blueprint("status", __name__)


@status_bp.route("/candidate/status/<int:candidate_id>/<status>")
def update_status(candidate_id, status):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    CandidateStatusService.update_status(
        candidate_id,
        status
    )

    flash("Candidate status updated successfully.")

    return redirect(
        url_for(
            "profile.profile",
            candidate_id=candidate_id
        )
    )