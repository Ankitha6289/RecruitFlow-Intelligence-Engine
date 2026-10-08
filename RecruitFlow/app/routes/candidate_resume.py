from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.utils import secure_filename
import os

from app.database.db import db
from app.models.candidate import Candidate

candidate_resume_bp = Blueprint(
    "candidate_resume",
    __name__
)

UPLOAD_FOLDER = "uploads/resumes"

ALLOWED_EXTENSIONS = {
    "pdf",
    "doc",
    "docx"
}


def allowed_file(filename):

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@candidate_resume_bp.route(
    "/candidate/upload",
    methods=["GET", "POST"]
)
def upload_resume():

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

        file = request.files.get("resume")

        if file is None or file.filename == "":

            flash(
                "Please choose a file.",
                "warning"
            )

            return redirect(request.url)

        if not allowed_file(file.filename):

            flash(
                "Only PDF, DOC and DOCX files are allowed.",
                "danger"
            )

            return redirect(request.url)

        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )

        # Delete old resume
        if candidate.resume_path:

            old_path = os.path.join(
                UPLOAD_FOLDER,
                candidate.resume_path
            )

            if os.path.exists(old_path):

                os.remove(old_path)

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        # Save filename only
        candidate.resume_path = filename

        db.session.commit()

        flash(
            "Resume uploaded successfully.",
            "success"
        )

        return redirect(
            url_for(
                "candidate_resume.upload_resume"
            )
        )

    return render_template(
        "candidates/upload_resume.html",
        candidate=candidate
    )