from app.database.db import db
from app.models.skills import Skill
from app.models.job import Job
from app.models.skill_gap import SkillGap
from app.models.candidate import Candidate


class SkillGapService:

    @staticmethod
    def analyze(candidate_id, job_id):

        candidate = db.session.get(Candidate, candidate_id)

        if not candidate:
            raise Exception(f"Candidate {candidate_id} does not exist.")

        job = db.session.get(Job, job_id)

        if not job:
            raise Exception(f"Job {job_id} does not exist.")

        candidate_skills = Skill.query.filter_by(
            candidate_id=candidate_id
        ).all()

        candidate_skill_list = [
            s.skill_name.lower()
            for s in candidate_skills
        ]

        job_skills = []

        if job.skills:
            job_skills = [
                x.strip().lower()
                for x in job.skills.split(",")
            ]

        matched = []
        missing = []

        for skill in job_skills:

            if skill in candidate_skill_list:
                matched.append(skill)
            else:
                missing.append(skill)

        if missing:
            recommendation = (
                "Candidate should improve: "
                + ", ".join(missing)
            )
        else:
            recommendation = (
                "Candidate matches all required skills."
            )

        old_report = SkillGap.query.filter_by(
            candidate_id=candidate_id,
            job_id=job_id
        ).first()

        if old_report:

            old_report.matched_skills = ", ".join(matched)
            old_report.missing_skills = ", ".join(missing)
            old_report.recommendation = recommendation

            db.session.commit()

            return old_report

        report = SkillGap(
            candidate_id=candidate_id,
            job_id=job_id,
            matched_skills=", ".join(matched),
            missing_skills=", ".join(missing),
            recommendation=recommendation
        )

        db.session.add(report)
        db.session.commit()

        return report