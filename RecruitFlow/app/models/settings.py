from app.database.db import db


class Settings(db.Model):

    __tablename__ = "settings"

    setting_id = db.Column(
        db.Integer,
        primary_key=True
    )

    company_name = db.Column(
        db.String(200),
        nullable=False
    )

    company_email = db.Column(
        db.String(200)
    )

    company_phone = db.Column(
        db.String(20)
    )

    company_address = db.Column(
        db.Text
    )

    company_logo = db.Column(
        db.String(255)
    )

    ai_model = db.Column(
        db.String(100),
        default="Gemini"
    )

    max_resume_size = db.Column(
        db.Integer,
        default=5
    )

    maintenance_mode = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    def __repr__(self):
        return f"<Settings {self.company_name}>"