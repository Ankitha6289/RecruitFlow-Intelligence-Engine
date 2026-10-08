from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_from_directory
)

from app.database.db import db

from app.models.candidate import Candidate
from app.models.education import Education
from app.models.experience import Experience
from app.models.skills import Skill

candidate_profile_bp = Blueprint(
    "candidate_profile",
    __name__
)


@candidate_profile_bp.route(
    "/candidate/profile",
    methods=["GET", "POST"]
)
def profile():

    if "candidate_id" not in session:
        return redirect(
            url_for("candidate_auth.login")
        )

    candidate = db.session.get(
        Candidate,
        session["candidate_id"]
    )

    if candidate is None:

        flash(
            "Candidate not found.",
            "danger"
        )

        return redirect(
            url_for("candidate_auth.login")
        )

    if request.method == "POST":

        candidate.full_name = request.form["full_name"]
        candidate.phone = request.form["phone"]
        candidate.address = request.form["address"]
        candidate.linkedin = request.form["linkedin"]
        candidate.github = request.form["github"]
        candidate.portfolio = request.form["portfolio"]

        db.session.commit()

        flash(
            "Profile Updated Successfully.",
            "success"
        )

        return redirect(
            url_for("candidate_profile.profile")
        )

    education = Education.query.filter_by(
        candidate_id=candidate.candidate_id
    ).all()

    experience = Experience.query.filter_by(
        candidate_id=candidate.candidate_id
    ).all()

    skills = Skill.query.filter_by(
        candidate_id=candidate.candidate_id
    ).all()

    return render_template(

        "candidates/profile.html",

        candidate=candidate,

        education=education,

        experience=experience,

        skills=skills

    )


@candidate_profile_bp.route(
    "/candidate/download/<int:candidate_id>"
)
def download_resume(candidate_id):

    if "candidate_id" not in session and "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    candidate = db.session.get(
        Candidate,
        candidate_id
    )

    if candidate is None or not candidate.resume_path:

        flash(
            "Resume not found.",
            "warning"
        )

        return redirect(
            url_for("candidate_profile.profile")
        )

    return send_from_directory(
        "uploads/resumes",
        candidate.resume_path,
        as_attachment=True
    )