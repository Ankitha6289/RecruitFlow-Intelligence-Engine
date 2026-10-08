from app.database.db import db


class ChatbotHistory(db.Model):

    __tablename__ = "chatbot_history"

    chat_id = db.Column(
        db.Integer,
        primary_key=True
    )

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey("candidates.candidate_id"),
        nullable=False
    )

    user_question = db.Column(
        db.Text,
        nullable=False
    )

    ai_answer = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    candidate = db.relationship(
        "Candidate",
        backref="chat_history"
    )

    def __repr__(self):
        return f"<Chat {self.chat_id}>"