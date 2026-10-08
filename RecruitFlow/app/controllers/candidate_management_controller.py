from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_from_directory
)

from app.models.candidate import Candidate
from app.services.candidate_management_service import CandidateManagementService
from app.database.db import db

candidate_management_bp = Blueprint(
    "candidate_management",
    __name__
)


# ==========================================
# Candidate List
# ==========================================

@candidate_management_bp.route("/admin/candidates")
def candidates():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "")
    status = request.args.get("status", "")
    skill = request.args.get("skill", "")
    min_score = request.args.get("min_score", "")

    candidates = CandidateManagementService.get_all(
        search,
        status,
        skill,
        min_score or None
    )

    score_summary = CandidateManagementService.get_score_summary()

    return render_template(
        "candidates/candidates.html",
        candidates=candidates,
        search=search,
        status=status,
        skill=skill,
        min_score=min_score,
        score_summary=score_summary
    )


# ==========================================
# Candidate Details
# ==========================================

@candidate_management_bp.route(
    "/admin/candidates/<int:candidate_id>"
)
def candidate_details(candidate_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    candidate = CandidateManagementService.get(candidate_id)

    if candidate is None:

        flash(
            "Candidate not found.",
            "danger"
        )

        return redirect(
            url_for("candidate_management.candidates")
        )

    education = candidate.education if candidate else []
    experience = candidate.experience if candidate else []
    skills = candidate.skills if candidate else []
    analysis = candidate.analysis[0] if candidate and candidate.analysis else None
    ats_analysis = None
    if candidate:
        ats_analysis = candidate.ats_analysis[0] if getattr(candidate, "ats_analysis", None) else None

    certifications = []
    projects = []
    languages = []
    achievements = []
    years_of_experience = ""

    if analysis is not None:
        certifications = [item.strip() for item in str(analysis.strengths or "").split(",") if item.strip()]
        projects = [item.strip() for item in str(analysis.recommended_roles or "").split(",") if item.strip()]
        languages = [item.strip() for item in str(analysis.weaknesses or "").split(",") if item.strip()]
        achievements = [item.strip() for item in str(analysis.candidate_summary or "").split(".") if item.strip()]
        years_of_experience = ""

    return render_template(
        "candidates/candidate_details.html",
        candidate=candidate,
        education=education,
        experience=experience,
        skills=skills,
        analysis=analysis,
        ats_analysis=ats_analysis,
        certifications=certifications,
        projects=projects,
        languages=languages,
        achievements=achievements,
        years_of_experience=years_of_experience
    )


# ==========================================
# Edit Candidate
# ==========================================

@candidate_management_bp.route(
    "/admin/candidates/scoring-dashboard"
)
def scoring_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    candidates = CandidateManagementService.get_all()
    data = CandidateManagementService.build_scoring_dashboard_data(candidates)

    return render_template(
        "scoring_dashboard.html",
        data=data
    )


@candidate_management_bp.route(
    "/admin/candidates/download/<int:candidate_id>"
)
def download_resume(candidate_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    candidate = db.session.get(Candidate, candidate_id)

    if candidate is None or not candidate.resume_path:
        flash("Resume not found.", "warning")
        return redirect(url_for("candidate_management.candidates"))

    return send_from_directory(
        "uploads/resumes",
        candidate.resume_path,
        as_attachment=True
    )


@candidate_management_bp.route(
    "/admin/candidates/edit/<int:candidate_id>",
    methods=["GET", "POST"]
)
def edit_candidate(candidate_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    candidate = CandidateManagementService.get(candidate_id)

    if candidate is None:

        flash(
            "Candidate not found.",
            "danger"
        )

        return redirect(
            url_for("candidate_management.candidates")
        )

    if request.method == "POST":

        CandidateManagementService.update(

            candidate_id,

            request.form["full_name"],

            request.form["email"],

            request.form["phone"],

            request.form["address"],

            request.form["linkedin"],

            request.form["github"],

            request.form["portfolio"],

            request.form["status"]

        )

        flash(
            "Candidate Updated Successfully.",
            "success"
        )

        return redirect(
            url_for("candidate_management.candidates")
        )

    return render_template(
        "candidates/edit_candidate.html",
        candidate=candidate
    )


# ==========================================
# Delete Candidate
# ==========================================

@candidate_management_bp.route(
    "/admin/candidates/delete/<int:candidate_id>"
)
def delete_candidate(candidate_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    CandidateManagementService.delete(candidate_id)

    flash(
        "Candidate Deleted Successfully.",
        "success"
    )

    return redirect(
        url_for("candidate_management.candidates")
    )


# ==========================================
# Export PDF
# ==========================================

@candidate_management_bp.route(
    "/admin/candidates/export/pdf"
)
def export_pdf():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return CandidateManagementService.export_pdf()


# ==========================================
# Export Excel
# ==========================================

@candidate_management_bp.route(
    "/admin/candidates/export/excel"
)
def export_excel():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return CandidateManagementService.export_excel()