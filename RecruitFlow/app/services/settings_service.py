from app.database.db import db
from app.models.settings import Settings


class SettingsService:

    # =====================================
    # Get Settings
    # =====================================

    @staticmethod
    def get():

        settings = Settings.query.first()

        if not settings:

            settings = Settings(

                company_name="RecruitFlow",

                company_email="admin@recruitflow.com",

                company_phone="9876543210",

                company_address="Company Address",

                ai_model="Gemini",

                max_resume_size=5,

                maintenance_mode=False

            )

            db.session.add(settings)

            db.session.commit()

        return settings

    # =====================================
    # Update Settings
    # =====================================

    @staticmethod
    def update(data):

        settings = Settings.query.first()

        if not settings:

            settings = Settings()

            db.session.add(settings)

        settings.company_name = data.get(
            "company_name"
        )

        settings.company_email = data.get(
            "company_email"
        )

        settings.company_phone = data.get(
            "company_phone"
        )

        settings.company_address = data.get(
            "company_address"
        )

        settings.ai_model = data.get(
            "ai_model"
        )

        settings.max_resume_size = int(
            data.get("max_resume_size", 5)
        )

        settings.maintenance_mode = (

            True if data.get("maintenance_mode")

            else False

        )

        db.session.commit()

        return settings