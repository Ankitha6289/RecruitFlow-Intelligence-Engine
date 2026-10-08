from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from app.database.db import db
from config import Config
from app.parser.extractor import ResumeExtractor
from app.parser.resume_parser import ResumeParser
from app.models.candidate import Candidate
from app.services.candidate_service import CandidateService

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"pdf", "docx"}


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@upload_bp.route("/")
def home():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("upload.html")


@upload_bp.route("/upload", methods=["POST"])
def upload_resume():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    files = request.files.getlist("resumes")

    if not files:
        flash("Please select one or more resumes.", "danger")
        return redirect(url_for("upload.home"))

    uploaded = 0
    failed = 0

    for file in files:

        if file.filename == "":
            continue

        if not allowed_file(file.filename):
            flash(f"{file.filename} is not a supported file.", "danger")
            failed += 1
            continue

        filename = secure_filename(file.filename)

        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

        filepath = os.path.join(
            Config.UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        try:

            # Extract Resume Text
            text = ResumeExtractor.extract(filepath)

            # Parse Resume
            parser = ResumeParser(text)

            parsed_data = parser.parse()

            # Save Candidate
            candidate = CandidateService.save_complete_candidate(parsed_data)

            if candidate is not None:
                candidate.resume_path = filename
                db.session.commit()

            uploaded += 1

        except Exception as e:

            db.session.rollback()

            failed += 1

            flash(
                f"{filename}: {str(e)}",
                "danger"
            )

    flash(
        f"Upload Completed. {uploaded} Resume(s) Uploaded Successfully. {failed} Failed.",
        "success"
    )

    return redirect(url_for("upload.home"))