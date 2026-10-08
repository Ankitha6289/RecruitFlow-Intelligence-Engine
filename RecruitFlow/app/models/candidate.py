from app.database.db import db

class Candidate(db.Model):

    __tablename__ = "candidates"

    candidate_id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(150), nullable=False)

    email = db.Column(db.String(120), unique=True)

    phone = db.Column(db.String(20))

    linkedin = db.Column(db.Text)

    github = db.Column(db.Text)

    portfolio = db.Column(db.Text)

    address = db.Column(db.Text)

    resume_path = db.Column(db.String(255))

    status = db.Column(
    db.String(50),
    default="Applied"
)

    education = db.relationship(
        "Education",
        backref="candidate",
        lazy=True
    )

    experience = db.relationship(
        "Experience",
        backref="candidate",
        lazy=True
    )

    skills = db.relationship(
        "Skill",
        backref="candidate",
        lazy=True
    )

    analysis = db.relationship(
        "AIAnalysis",
        backref="candidate",
        lazy=True
    )
    password = db.Column(
    db.String(255),
    nullable=False
)