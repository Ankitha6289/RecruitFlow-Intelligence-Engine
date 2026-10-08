from werkzeug.security import generate_password_hash

from app.database.db import db

from app.models.candidate import Candidate
from app.models.education import Education
from app.models.experience import Experience
from app.models.skills import Skill

from app.services.ai_analysis_service import AIAnalysisService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService
from app.services.ats_service import ATSService


class CandidateService:

    # =====================================================
    # Save Candidate
    # =====================================================

    @staticmethod
    def save_candidate(data):

        candidate = Candidate.query.filter_by(
            email=data.get("email")
        ).first()

        if candidate:
            # Update existing candidate with any new info
            candidate.full_name  = data.get("full_name")  or candidate.full_name
            candidate.phone      = data.get("phone")      or candidate.phone
            candidate.linkedin   = data.get("linkedin")   or candidate.linkedin
            candidate.github     = data.get("github")     or candidate.github
            candidate.portfolio  = data.get("portfolio")  or candidate.portfolio
            candidate.address    = data.get("address")    or candidate.address
            candidate.status     = candidate.status       or "Applied"
            db.session.commit()
            return candidate

        candidate = Candidate(
            full_name  = data.get("full_name"),
            email      = data.get("email"),
            phone      = data.get("phone"),
            linkedin   = data.get("linkedin"),
            github     = data.get("github"),
            portfolio  = data.get("portfolio"),
            address    = data.get("address", ""),
            status     = "Applied",
            password   = generate_password_hash("candidate123")
        )

        db.session.add(candidate)
        db.session.commit()

        NotificationService.create(
            title="New Candidate",
            message=f"Candidate {candidate.full_name} registered.",
            notification_type="Candidate",
            recipient_role="Recruiter"
        )

        return candidate

    # =====================================================
    # Save Education
    # =====================================================

    @staticmethod
    def save_education(candidate_id, education_list):

        for item in education_list:
            db.session.add(Education(
                candidate_id = candidate_id,
                degree       = item,
                institution  = "",
                year         = "",
                cgpa         = ""
            ))

        db.session.commit()

    # =====================================================
    # Save Experience
    # =====================================================

    @staticmethod
    def save_experience(candidate_id, experience_list):

        for item in experience_list:
            db.session.add(Experience(
                candidate_id = candidate_id,
                company_name = "",
                role         = item,
                duration     = "",
                description  = ""
            ))

        db.session.commit()

    # =====================================================
    # Save Skills
    # =====================================================

    @staticmethod
    def save_skills(candidate_id, skills):

        for skill_name in skills:
            db.session.add(Skill(
                candidate_id = candidate_id,
                skill_name   = skill_name,
                skill_type   = "Technical"
            ))

        db.session.commit()

    # =====================================================
    # Save Complete Candidate  (called from upload route)
    # =====================================================

    @staticmethod
    def save_complete_candidate(data):

        try:
            candidate = CandidateService.save_candidate(data)

            CandidateService.save_education(
                candidate.candidate_id,
                data.get("education", [])
            )

            CandidateService.save_experience(
                candidate.candidate_id,
                data.get("experience", [])
            )

            CandidateService.save_skills(
                candidate.candidate_id,
                data.get("skills", [])
            )

            AIAnalysisService.analyze_and_save(
                candidate.candidate_id,
                data
            )

            ATSService.analyze(candidate.candidate_id)

            db.session.commit()

            # System-level activity log (no user — triggered by upload)
            ActivityLogService.create(
                user_id  = None,
                activity = f"Resume uploaded: {candidate.full_name}",
                module   = "Resume Upload"
            )

            NotificationService.create(
                title             = "Resume Uploaded",
                message           = f"{candidate.full_name}'s resume processed successfully.",
                notification_type = "Resume",
                recipient_role    = "Recruiter"
            )

            return candidate

        except Exception:
            db.session.rollback()
            raise
