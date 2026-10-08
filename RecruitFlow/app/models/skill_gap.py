from app.database.db import db


class SkillGap(db.Model):

    __tablename__ = "skill_gap"

    gap_id = db.Column(
        db.Integer,
        primary_key=True
    )

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey("candidates.candidate_id")
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.job_id")
    )

    matched_skills = db.Column(db.Text)

    missing_skills = db.Column(db.Text)

    recommendation = db.Column(db.Text)