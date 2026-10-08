from app.database.db import db

class Experience(db.Model):

    __tablename__ = "experience"

    experience_id = db.Column(db.Integer, primary_key=True)

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey("candidates.candidate_id")
    )

    company_name = db.Column(db.String(200))

    role = db.Column(db.String(150))

    duration = db.Column(db.String(100))

    description = db.Column(db.Text)