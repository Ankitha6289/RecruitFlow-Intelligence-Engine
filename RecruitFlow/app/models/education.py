from app.database.db import db

class Education(db.Model):

    __tablename__ = "education"

    education_id = db.Column(db.Integer, primary_key=True)

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey("candidates.candidate_id")
    )

    degree = db.Column(db.String(150))

    institution = db.Column(db.String(200))

    year = db.Column(db.String(20))

    cgpa = db.Column(db.String(20))