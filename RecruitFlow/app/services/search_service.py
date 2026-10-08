from sqlalchemy import or_

from app.models.candidate import Candidate
from app.models.skills import Skill


class SearchService:

    @staticmethod
    def search_candidates(keyword):

        return Candidate.query.filter(

            or_(

                Candidate.full_name.ilike(f"%{keyword}%"),

                Candidate.email.ilike(f"%{keyword}%"),

                Candidate.phone.ilike(f"%{keyword}%")

            )

        ).all()

    @staticmethod
    def search_by_skill(keyword):

        return Skill.query.filter(

            Skill.skill_name.ilike(f"%{keyword}%")

        ).all()