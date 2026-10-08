from app.database.db import db


class InterviewQuestion(db.Model):
    __tablename__ = "interview_questions"

    question_id = db.Column(
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

    hr_questions = db.Column(
        db.Text,
        nullable=False
    )

    technical_questions = db.Column(
        db.Text,
        nullable=False
    )

    coding_questions = db.Column(
        db.Text,
        nullable=False
    )

    scenario_questions = db.Column(
        db.Text,
        nullable=False
    )

    behavioral_questions = db.Column(
        db.Text,
        nullable=False
    )

    evaluation = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    candidate = db.relationship(
        "Candidate",
        backref="interview_reports"
    )

    job = db.relationship(
        "Job",
        backref="interview_reports"
    )