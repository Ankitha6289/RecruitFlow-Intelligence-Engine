import json
from sqlalchemy import func
from collections import Counter

from app.database.db import db

from app.models.user import User
from app.models.job import Job
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.models.offer import Offer
from app.models.ai_analysis import AIAnalysis
from app.models.skills import Skill


class AdminDashboardService:

    @staticmethod
    def get_dashboard_data():

        # -----------------------------
        # Dashboard Cards
        # -----------------------------

        total_users = User.query.count()

        total_recruiters = User.query.filter_by(
            role="Recruiter"
        ).count()

        total_candidates = Candidate.query.count()

        total_jobs = Job.query.count()

        total_interviews = Interview.query.count()

        total_offers = Offer.query.count()

        total_ai_analysis = AIAnalysis.query.count()

        average_score = db.session.query(
            func.avg(AIAnalysis.suitability_scores)
        ).scalar() or 0

        # -----------------------------
        # Candidate Status
        # -----------------------------

        applied = Candidate.query.filter_by(
            status="Applied"
        ).count()

        selected = Candidate.query.filter_by(
            status="Selected"
        ).count()

        rejected = Candidate.query.filter_by(
            status="Rejected"
        ).count()

        # -----------------------------
        # Interview Status
        # -----------------------------

        scheduled = Interview.query.filter_by(
            status="Scheduled"
        ).count()

        completed = Interview.query.filter_by(
            status="Completed"
        ).count()

        # -----------------------------
        # Offer Status
        # -----------------------------

        pending = Offer.query.filter_by(
            status="Pending"
        ).count()

        accepted = Offer.query.filter_by(
            status="Accepted"
        ).count()

        declined = Offer.query.filter_by(
            status="Declined"
        ).count()

        # -----------------------------
        # Job Status
        # -----------------------------

        active_jobs = Job.query.filter_by(
            status="Active"
        ).count()

        closed_jobs = Job.query.filter_by(
            status="Closed"
        ).count()

        # -----------------------------
        # Top Skills
        # -----------------------------

        counter = Counter()

        for skill in Skill.query.all():
            counter[skill.skill_name] += 1

        top_skills = counter.most_common(10)

        # -----------------------------
        # AI Recommended Roles (with candidate info)
        # -----------------------------

        recommended_roles_raw = (
            db.session.query(AIAnalysis, Candidate)
            .join(Candidate, AIAnalysis.candidate_id == Candidate.candidate_id)
            .filter(AIAnalysis.recommended_roles != None)
            .order_by(AIAnalysis.analysis_id.desc())
            .limit(5)
            .all()
        )

        recommended_roles = []
        for analysis, candidate in recommended_roles_raw:
            if not analysis.recommended_roles:
                continue

            roles = []
            import json as _json
            try:
                parsed = json.loads(analysis.recommended_roles)
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

            recommended_roles.append({
                "name": candidate.full_name,
                "email": candidate.email,
                "roles": roles,
            })

        # -----------------------------
        # Recent Data
        # -----------------------------

        recent_users = User.query.order_by(
            User.user_id.desc()
        ).limit(5).all()

        recent_candidates = Candidate.query.order_by(
            Candidate.candidate_id.desc()
        ).limit(5).all()

        recent_jobs = Job.query.order_by(
            Job.job_id.desc()
        ).limit(5).all()

        recent_interviews = Interview.query.order_by(
            Interview.interview_id.desc()
        ).limit(5).all()

        recent_offers = Offer.query.order_by(
            Offer.offer_id.desc()
        ).limit(5).all()

        # Offer acceptance rate
        total_evaluated_offers = accepted + declined
        offer_acceptance_rate = (
            round((accepted / total_evaluated_offers) * 100, 1)
            if total_evaluated_offers > 0 else 0
        )

        # Selection rate (selected / total candidates)
        selection_rate = (
            round((selected / total_candidates) * 100, 1)
            if total_candidates > 0 else 0
        )

        # System user counts
        total_system_users = total_users
        admin_count = User.query.filter_by(role="Admin").count()

        # -----------------------------
        # Return
        # -----------------------------

        return {

            "total_users": total_users,

            "total_recruiters": total_recruiters,

            "total_candidates": total_candidates,

            "total_jobs": total_jobs,

            "total_interviews": total_interviews,

            "total_offers": total_offers,

            "total_ai_analysis": total_ai_analysis,

            "average_score": round(float(average_score), 2),

            "applied": applied,

            "selected": selected,

            "rejected": rejected,

            "scheduled": scheduled,

            "completed": completed,

            "pending_offers": pending,

            "accepted_offers": accepted,

            "declined_offers": declined,

            "active_jobs": active_jobs,

            "closed_jobs": closed_jobs,

            "top_skills": top_skills,

            "recommended_roles": recommended_roles,

            "recent_users": recent_users,

            "recent_jobs": recent_jobs,

            "recent_interviews": recent_interviews,

            "recent_offers": recent_offers,

            "recent_candidates": recent_candidates,

            "offer_acceptance_rate": offer_acceptance_rate,

            "selection_rate": selection_rate,

            "total_system_users": total_system_users,

            "admin_count": admin_count,

        }