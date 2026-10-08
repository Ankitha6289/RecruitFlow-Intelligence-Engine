from app.database.db import db


class ActivityLog(db.Model):

    __tablename__ = "activity_logs"

    log_id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=True
    )

    activity = db.Column(
        db.String(255),
        nullable=False
    )

    module = db.Column(
        db.String(100)
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user = db.relationship(
        "User",
        backref="activity_logs"
    )

    def __repr__(self):
        return f"<ActivityLog {self.activity}>"