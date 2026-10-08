from app.database.db import db

from app.models.candidate import Candidate
from app.models.job import Job
from app.models.skills import Skill
from app.models.job_match import JobMatch


class JobMatchingService:

    @staticmethod
    def calculate_match(candidate_id, job_id):

        candidate = db.session.get(Candidate, candidate_id)
        job = db.session.get(Job, job_id)

        if not candidate or not job:
            return None

        # Candidate Skills
        candidate_skills = [

            skill.skill_name.lower().strip()

            for skill in Skill.query.filter_by(
                candidate_id=candidate_id
            ).all()

        ]

        # Job Skills
        job_skills = [

            skill.strip().lower()

            for skill in job.skills.split(",")

            if skill.strip()

        ]

        # Matched Skills
        matched_skills = [

            skill

            for skill in job_skills

            if skill in candidate_skills

        ]

        # Missing Skills
        missing_skills = [

            skill

            for skill in job_skills

            if skill not in candidate_skills

        ]

        # Match Percentage
        score = 0

        if len(job_skills) > 0:

            score = round(

                (len(matched_skills) / len(job_skills)) * 100,

                2

            )

        # Recommended Role
        if score >= 80:

            recommended_role = job.title

        elif score >= 60:

            recommended_role = "Junior " + job.title

        elif score >= 40:

            recommended_role = "Intern - " + job.title

        else:

            recommended_role = "Skill Improvement Required"

        # Save Result
        report = JobMatch(

            candidate_id=candidate_id,

            job_id=job_id,

            matching_percentage=score,

            matched_skills=", ".join(matched_skills),

            missing_skills=", ".join(missing_skills),

            recommended_role=recommended_role

        )

        db.session.add(report)

        db.session.commit()

        return {

            "candidate": candidate,

            "job": job,

            "score": score,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "recommended_role": recommended_role

        }

    @staticmethod
    def get_best_matching_job(candidate_id):
        """Find the best matching job for a candidate based on skills"""
        candidate = db.session.get(Candidate, candidate_id)
        if not candidate:
            return None

        candidate_skills = {
            skill.skill_name.lower().strip()
            for skill in Skill.query.filter_by(candidate_id=candidate_id).all()
            if skill.skill_name and skill.skill_name.strip()
        }
        if not candidate_skills:
            return None

        jobs = Job.query.all()
        best_match = None
        best_score = -1

        for job in jobs:
            # Calculate match score for this job
            job_skills = [
                skill.strip().lower()
                for skill in (job.skills or "").split(",")
                if skill.strip()
            ]
            if not job_skills:
                continue

            matched_skills = [
                skill for skill in job_skills if skill in candidate_skills
            ]

            score = 0
            if len(job_skills) > 0:
                score = round((len(matched_skills) / len(job_skills)) * 100, 2)

            if score > best_score:
                best_score = score
                best_match = {
                    "job": job,
                    "score": score,
                    "matched_skills": matched_skills
                }

        return best_match