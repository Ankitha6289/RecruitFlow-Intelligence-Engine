from app.database.db import db


class AIInterview(db.Model):

    __tablename__ = "ai_interviews"

    interview_id = db.Column(
        db.Integer,
        primary_key=True
    )

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey("candidates.candidate_id"),
        nullable=False
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.job_id"),
        nullable=False
    )

    interview_link = db.Column(
        db.String(255)
    )

    scheduled_date = db.Column(
        db.Date
    )

    scheduled_time = db.Column(
        db.Time
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    candidate = db.relationship(
        "Candidate",
        backref="ai_interviews"
    )

    job = db.relationship(
        "Job",
        backref="ai_interviews"
    )