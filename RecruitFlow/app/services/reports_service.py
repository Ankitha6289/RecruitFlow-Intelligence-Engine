from sqlalchemy import func

from app.database.db import db

from app.models.application import Application
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.models.offer import Offer
from app.models.skills import Skill
from app.models.ai_analysis import AIAnalysis
from app.models.job import Job


class ReportsService:

    @staticmethod
    def get_dashboard_data():

        # ==========================
        # Monthly Applications
        # ==========================

        monthly = (
            db.session.query(
                func.month(Application.applied_date),
                func.count(Application.application_id)
            )
            .group_by(func.month(Application.applied_date))
            .all()
        )

        monthly_labels = []
        monthly_values = []

        for month, total in monthly:
            monthly_labels.append(str(month))
            monthly_values.append(total)

        # ==========================
        # Candidate Status
        # ==========================

        applied = Candidate.query.filter_by(
            status="Applied"
        ).count()

        selected = Candidate.query.filter_by(
            status="Selected"
        ).count()

        rejected = Candidate.query.filter_by(
            status="Rejected"
        ).count()

        # ==========================
        # Interview Status
        # ==========================

        scheduled = Interview.query.filter_by(
            status="Scheduled"
        ).count()

        completed = Interview.query.filter_by(
            status="Completed"
        ).count()

        selected_interview = Interview.query.filter_by(
            status="Selected"
        ).count()

        rejected_interview = Interview.query.filter_by(
            status="Rejected"
        ).count()

        # ==========================
        # Offer Status
        # ==========================

        pending = Offer.query.filter_by(
            status="Pending"
        ).count()

        accepted = Offer.query.filter_by(
            status="Accepted"
        ).count()

        declined = Offer.query.filter_by(
            status="Declined"
        ).count()

        # ==========================
        # Top Skills
        # ==========================

        skills = (
            db.session.query(
                Skill.skill_name,
                func.count(Skill.skill_id)
            )
            .group_by(Skill.skill_name)
            .order_by(func.count(Skill.skill_id).desc())
            .limit(10)
            .all()
        )

        skill_labels = []
        skill_values = []

        for skill, count in skills:
            skill_labels.append(skill)
            skill_values.append(count)

        # ==========================
        # Job Wise Applications
        # ==========================

        jobs = (
            db.session.query(
                Job.title,
                func.count(Application.application_id)
            )
            .join(Application)
            .group_by(Job.title)
            .all()
        )

        job_labels = []
        job_values = []

        for job, total in jobs:
            job_labels.append(job)
            job_values.append(total)

        # ==========================
        # Average AI Score
        # ==========================

        avg_ai = db.session.query(
            func.avg(AIAnalysis.suitability_score)
        ).scalar() or 0

        return {

            "monthly_labels": monthly_labels,
            "monthly_values": monthly_values,

            "candidate_status": [
                applied,
                selected,
                rejected
            ],

            "interview_status": [
                scheduled,
                completed,
                selected_interview,
                rejected_interview
            ],

            "offer_status": [
                pending,
                accepted,
                declined
            ],

            "skill_labels": skill_labels,
            "skill_values": skill_values,

            "job_labels": job_labels,
            "job_values": job_values,

            "average_ai": round(float(avg_ai), 2)

        }