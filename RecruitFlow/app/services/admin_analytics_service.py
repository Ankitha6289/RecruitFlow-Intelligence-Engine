from app.models.candidate import Candidate
from app.models.job import Job
from app.models.application import Application
from app.models.interview import Interview
from app.models.offer import Offer


class AdminAnalyticsService:

    @staticmethod
    def get_dashboard():

        return {

            "total_candidates": Candidate.query.count(),

            "total_jobs": Job.query.count(),

            "total_applications": Application.query.count(),

            "total_interviews": Interview.query.count(),

            "total_offers": Offer.query.count(),

            "selected_candidates":
                Candidate.query.filter_by(
                    status="Hired"
                ).count(),

            "rejected_candidates":
                Candidate.query.filter_by(
                    status="Rejected"
                ).count()

        }