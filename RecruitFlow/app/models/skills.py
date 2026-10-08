from app.database.db import db

class Skill(db.Model):

    __tablename__ = "skills"

    skill_id = db.Column(db.Integer, primary_key=True)

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey("candidates.candidate_id")
        
    )

    skill_name = db.Column(db.String(150))

    skill_type = db.Column(db.String(100))