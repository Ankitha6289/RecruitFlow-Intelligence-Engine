from app.database.db import db

from app.models.candidate import Candidate
from app.models.ai_analysis import AIAnalysis
from app.models.ats_analysis import ATSAnalysis
from app.models.interview_questions import InterviewQuestion
from app.models.application import Application
from app.models.interview import Interview
from app.models.offer import Offer


class CandidateDashboardService:

    @staticmethod
    def get_dashboard(candidate_id):

        candidate = db.session.get(
            Candidate,
            candidate_id
        )

        analysis = AIAnalysis.query.filter_by(
            candidate_id=candidate_id
        ).first()

        ats_analysis = ATSAnalysis.query.filter_by(
            candidate_id=candidate_id
        ).first()
        

        question_count = InterviewQuestion.query.filter_by(
            candidate_id=candidate_id
        ).count()

        applications = Application.query.filter_by(
            candidate_id=candidate_id
        ).count()

        interviews = Interview.query.filter_by(
            candidate_id=candidate_id
        ).count()

        upcoming_interview = Interview.query.filter_by(
            candidate_id=candidate_id,
            status="Scheduled"
        ).order_by(
            Interview.interview_date.asc(),
            Interview.interview_time.asc()
        ).first()

        offers = Offer.query.filter_by(
            candidate_id=candidate_id
        ).count()

        return {

            "candidate": candidate,

            "analysis": analysis,

            "ats_analysis": ats_analysis,

            "upcoming_interview": upcoming_interview,

            "question_count": question_count,

            "application_count": applications,

            "interview_count": interviews,

            "offer_count": offers

        }