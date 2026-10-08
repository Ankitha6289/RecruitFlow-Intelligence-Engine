from app.database.db import db

from app.models.candidate import Candidate
from app.models.education import Education
from app.models.experience import Experience
from app.models.skills import Skill


class CandidateProfileService:

    @staticmethod
    def get_candidate(candidate_id):

        return db.session.get(
            Candidate,
            candidate_id
        )

    @staticmethod
    def get_education(candidate_id):

        return Education.query.filter_by(
            candidate_id=candidate_id
        ).all()

    @staticmethod
    def get_experience(candidate_id):

        return Experience.query.filter_by(
            candidate_id=candidate_id
        ).all()

    @staticmethod
    def get_skills(candidate_id):

        return Skill.query.filter_by(
            candidate_id=candidate_id
        ).all()

    @staticmethod
    def update_profile(

        candidate_id,

        full_name,

        phone,

        address,

        linkedin,

        github,

        portfolio

    ):

        candidate = db.session.get(
            Candidate,
            candidate_id
        )

        if candidate is None:
            return None

        candidate.full_name = full_name
        candidate.phone = phone
        candidate.address = address
        candidate.linkedin = linkedin
        candidate.github = github
        candidate.portfolio = portfolio

        db.session.commit()

        return candidate