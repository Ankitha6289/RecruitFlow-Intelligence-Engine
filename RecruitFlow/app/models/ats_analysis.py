from app.database.db import db

class ATSAnalysis(db.Model):
    __tablename__ = "ats_analysis"

    ats_id = db.Column(db.Integer, primary_key=True)

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey("candidates.candidate_id"),
        nullable=False
    )

    ats_score = db.Column(db.Integer)

    matched_keywords = db.Column(db.Text)

    missing_keywords = db.Column(db.Text)

    suggestions = db.Column(db.Text)

    candidate = db.relationship(
        "Candidate",
        backref="ats_analysis"
    )