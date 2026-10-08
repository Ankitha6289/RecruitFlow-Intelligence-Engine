from app.database.db import db


class AIInterviewResult(db.Model):

    __tablename__ = "ai_interview_results"

    result_id = db.Column(
        db.Integer,
        primary_key=True
    )

    interview_id = db.Column(
        db.Integer,
        db.ForeignKey("ai_interviews.interview_id")
    )

    question = db.Column(
        db.Text
    )

    answer = db.Column(
        db.Text
    )

    ai_score = db.Column(
        db.Float
    )

    feedback = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )