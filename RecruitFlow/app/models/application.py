from app.database.db import db

class Application(db.Model):

    __tablename__ = "applications"

    application_id = db.Column(
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

    status = db.Column(
        db.String(50),
        default="Applied"
    )

    remarks = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    candidate = db.relationship(
        "Candidate",
        backref="applications"
    )

    job = db.relationship(
        "Job",
        backref="applications"
    )

    def __repr__(self):
        return f"<Application {self.application_id}>"