from app.database.db import db


class AIAnalysis(db.Model):

    __tablename__ = "ai_analysis"

    analysis_id = db.Column(
        db.Integer,
        primary_key=True
    )

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey("candidates.candidate_id"),
        nullable=False
    )

    candidate_summary = db.Column(db.Text)

    recommended_roles = db.Column(db.Text)

    suitability_scores = db.Column(db.Text)

    strengths = db.Column(db.Text)

    weaknesses = db.Column(db.Text)