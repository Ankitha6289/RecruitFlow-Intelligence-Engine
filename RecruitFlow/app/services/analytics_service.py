from app.models.candidate import Candidate
from app.models.job import Job
from app.models.ai_analysis import AIAnalysis
from app.models.interview import Interview
from app.models.offer import Offer
from app.models.application import Application


class AnalyticsService:

    @staticmethod
    def dashboard():

        return {

            "total_candidates": Candidate.query.count(),

            "total_jobs": Job.query.count(),

            "total_ai": AIAnalysis.query.count(),

            "total_interviews": Interview.query.count(),

            "total_offers": Offer.query.count(),

            "total_applications": Application.query.count(),

            "selected_candidates":
                Application.query.filter_by(
                    status="Selected"
                ).count(),

            "rejected_candidates":
                Application.query.filter_by(
                    status="Rejected"
                ).count(),

            "shortlisted_candidates":
                Application.query.filter_by(
                    status="Shortlisted"
                ).count(),

            "pending_candidates":
                Application.query.filter_by(
                    status="Pending"
                ).count()

        }