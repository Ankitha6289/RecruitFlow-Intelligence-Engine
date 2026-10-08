from app.database.db import db


class Interview(db.Model):

    __tablename__ = "interviews"

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

    interviewer = db.Column(
        db.String(100),
        nullable=False
    )

    interview_date = db.Column(
        db.Date,
        nullable=False
    )

    interview_time = db.Column(
        db.Time,
        nullable=False
    )

    mode = db.Column(
        db.String(50),
        nullable=False
    )

    meeting_link = db.Column(
        db.String(255)
    )

    status = db.Column(
        db.String(50),
        default="Scheduled"
    )

    ai_final_score = db.Column(db.Float)
    ai_transcript = db.Column(db.Text)
    ai_recording_path = db.Column(db.String(255))
    ai_duration_seconds = db.Column(db.Integer)

    candidate = db.relationship(
        "Candidate",
        backref="interviews",
        lazy=True
    )

    job = db.relationship(
        "Job",
        backref="interviews",
        lazy=True
    )