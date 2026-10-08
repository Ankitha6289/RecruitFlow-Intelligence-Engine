from app.database.db import db


class Offer(db.Model):

    __tablename__ = "offers"

    offer_id = db.Column(
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

    offer_date = db.Column(
        db.Date,
        nullable=False
    )

    joining_date = db.Column(
        db.Date,
        nullable=False
    )

    salary = db.Column(
        db.String(100),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    pdf_path = db.Column(
        db.String(255)
    )

    candidate = db.relationship(
        "Candidate",
        backref="offers"
    )

    job = db.relationship(
        "Job",
        backref="offers"
    )