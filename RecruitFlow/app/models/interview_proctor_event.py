from app.database.db import db


class InterviewProctorEvent(db.Model):

    __tablename__ = "interview_proctor_events"

    event_id = db.Column(
        db.Integer,
        primary_key=True
    )

    interview_id = db.Column(
        db.Integer,
        db.ForeignKey("interviews.interview_id"),
        nullable=False
    )

    event_type = db.Column(
        db.String(100),
        nullable=False
    )

    details = db.Column(
        db.Text
    )

    severity = db.Column(
        db.String(20),
        default="low"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    interview = db.relationship(
        "Interview",
        backref="proctor_events"
    )
