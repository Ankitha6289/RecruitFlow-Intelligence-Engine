from app.database.db import db


class Job(db.Model):

    __tablename__ = "jobs"

    job_id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    company = db.Column(
        db.String(200)
    )

    location = db.Column(
        db.String(100)
    )

    experience = db.Column(
        db.String(100)
    )

    salary = db.Column(
        db.String(100)
    )

    skills = db.Column(
        db.Text
    )

    description = db.Column(
        db.Text
    )