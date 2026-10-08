from app.models.candidate import Candidate
from app.models.education import Education
from app.models.experience import Experience
from app.models.skills import Skill
from app.models.ai_analysis import AIAnalysis


class ProfileService:

    @staticmethod
    def get_candidate_profile(candidate_id):

        candidate = Candidate.query.get_or_404(candidate_id)

        education = Education.query.filter_by(
            candidate_id=candidate_id
        ).all()

        experience = Experience.query.filter_by(
            candidate_id=candidate_id
        ).all()

        skills = Skill.query.filter_by(
            candidate_id=candidate_id
        ).all()

        analysis = AIAnalysis.query.filter_by(
            candidate_id=candidate_id
        ).first()

        return {
            "candidate": candidate,
            "education": education,
            "experience": experience,
            "skills": skills,
            "analysis": analysis
        }