from app.database.db import db


class Job(db.Model):

    __tablename__ = "jobs"

    # ==========================================
    # Primary Key
    # ==========================================

    job_id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================================
    # Recruiter ID
    # ==========================================

    recruiter_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=True,
        index=True
    )

    # ==========================================
    # Job Details
    # ==========================================

    title = db.Column(
        db.String(200),
        nullable=False
    )

    company = db.Column(
        db.String(200),
        nullable=False
    )

    location = db.Column(
        db.String(200)
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

    # ==========================================
    # Job Status
    # ==========================================

    status = db.Column(
        db.String(20),
        default="Active",
        index=True
    )

    # ==========================================
    # Created Date
    # ==========================================

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # ==========================================
    # Recruiter Relationship
    # ==========================================

    recruiter = db.relationship(
        "User",
        backref="jobs",
        foreign_keys=[recruiter_id]
    )

    # ==========================================
    # Representation
    # ==========================================

    def __repr__(self):

        return f"<Job {self.job_id}: {self.title}>"