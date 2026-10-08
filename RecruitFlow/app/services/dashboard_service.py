from sqlalchemy import func

from app.database.db import db

from app.models.candidate import Candidate
from app.models.skills import Skill
from app.models.ai_analysis import AIAnalysis
from app.models.user import User
from app.models.interview import Interview
from app.models.job import Job
from app.models.offer import Offer


class DashboardService:

    @staticmethod
    def get_dashboard_data():

        # Dashboard Counts
        total_candidates = Candidate.query.count()

        total_skills = Skill.query.count()

        total_ai_analysis = AIAnalysis.query.count()

        total_recruiters = User.query.filter_by(
            role="Recruiter"
        ).count()

        total_jobs = Job.query.count()

        total_interviews = Interview.query.count()

        total_offers = Offer.query.count()

        # Interview Status Counts
        scheduled = Interview.query.filter_by(
            status="Scheduled"
        ).count()

        completed = Interview.query.filter_by(
            status="Completed"
        ).count()

        selected = Interview.query.filter_by(
            status="Selected"
        ).count()

        rejected = Interview.query.filter_by(
            status="Rejected"
        ).count()

        # Offer Status Counts
        pending_offers = Offer.query.filter_by(
            status="Pending"
        ).count()

        accepted_offers = Offer.query.filter_by(
            status="Accepted"
        ).count()

        declined_offers = Offer.query.filter_by(
            status="Declined"
        ).count()

        # Average AI Score
        avg_score = db.session.query(
            func.avg(AIAnalysis.suitability_scores)
        ).scalar()

        # Top Skills
        top_skills_query = (
            db.session.query(
                Skill.skill_name,
                func.count(Skill.skill_name)
            )
            .group_by(
                Skill.skill_name
            )
            .order_by(
                func.count(Skill.skill_name).desc()
            )
            .limit(10)
            .all()
        )
        top_skills = [(row[0], row[1]) for row in top_skills_query]


        # AI Recommended Roles
        recommended_roles_raw = AIAnalysis.query.order_by(
            AIAnalysis.analysis_id.desc()
        ).limit(5).all()

        recommended_roles = []
        for analysis in recommended_roles_raw:
            if not analysis.recommended_roles:
                continue

            roles = []
            try:
                import json as _json
                parsed = _json.loads(analysis.recommended_roles)
                if isinstance(parsed, list):
                    roles = [str(r).strip() for r in parsed if str(r).strip()][:3]
                elif isinstance(parsed, str):
                    roles = [parsed.strip()] if parsed.strip() else []
                else:
                    roles = [str(parsed).strip()] if str(parsed).strip() else []
            except Exception:
                raw_roles = str(analysis.recommended_roles)
                parts = [p.strip() for p in raw_roles.replace("\n", ",").split(",") if p.strip()]
                roles = parts[:3]

            if not roles:
                continue

            candidate = analysis.candidate if hasattr(analysis, 'candidate') else None
            recommended_roles.append({
                "name": candidate.full_name if candidate else "Candidate",
                "email": candidate.email if candidate else "",
                "roles": roles,
            })

        return {

            "total_candidates": total_candidates,

            "total_skills": total_skills,

            "total_ai_analysis": total_ai_analysis,

            "total_recruiters": total_recruiters,

            "total_jobs": total_jobs,

            "total_interviews": total_interviews,

            "total_offers": total_offers,

            "scheduled": scheduled,

            "completed": completed,

            "selected": selected,

            "rejected": rejected,

            "pending_offers": pending_offers,

            "accepted_offers": accepted_offers,

            "declined_offers": declined_offers,

            "average_score": round(float(avg_score or 0), 2),

            "top_skills": top_skills,

            "recommended_roles": recommended_roles

        }