from flask import (
    Blueprint,
    send_from_directory
)

file_bp = Blueprint(
    "file",
    __name__
)


@file_bp.route("/uploads/resumes/<filename>")
def uploaded_resume(filename):

    return send_from_directory(
        "uploads/resumes",
        filename
    )