from app.models.candidate import Candidate
from app.services.job_matching_service import JobMatchingService


class RankingService:

    @staticmethod
    def rank_candidates(job_id):

        candidates = Candidate.query.all()

        rankings = []

        for candidate in candidates:

            result = JobMatchingService.calculate_match(
                candidate.candidate_id,
                job_id
            )

            if result:

                rankings.append({

                    "candidate": candidate,

                    "score": result["score"],

                    "matched_skills": result["matched_skills"],

                    "missing_skills": result["missing_skills"]

                })

        rankings.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return rankings