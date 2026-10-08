from app.models.job import Job
from app.models.candidate import Candidate
from app.models.application import Application
from app.models.interview import Interview
from app.models.offer import Offer
from app.models.interview_proctor_event import InterviewProctorEvent


class RecruiterDashboardService:

    @staticmethod
    def get_dashboard():

        return {

            "jobs": Job.query.count(),

            "candidates": Candidate.query.count(),

            "applications": Application.query.count(),

            "interviews": Interview.query.count(),

            "offers": Offer.query.count(),

            "proctor_violations": InterviewProctorEvent.query.count()

        }