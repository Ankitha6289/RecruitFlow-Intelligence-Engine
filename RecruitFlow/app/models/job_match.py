from app.database.db import db


class JobMatch(db.Model):

    __tablename__ = "job_match"

    match_id = db.Column(
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

    matching_percentage = db.Column(
        db.Float
    )

    matched_skills = db.Column(
        db.Text
    )

    missing_skills = db.Column(
        db.Text
    )

    recommended_role = db.Column(
        db.String(200)
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    candidate = db.relationship(
        "Candidate",
        backref="job_matches"
    )

    job = db.relationship(
        "Job",
        backref="job_matches"
    )

    def __repr__(self):
        return f"<JobMatch {self.match_id}>"