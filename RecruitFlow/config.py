import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = "your_secret_key"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:anki2003@localhost/recruitflow"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 20,
        "max_overflow": 30,
        "pool_pre_ping": True,
        "pool_recycle": 1800,
    }

    UPLOAD_FOLDER = "uploads"

    # GROQ
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # Zoom Server-to-Server OAuth
    ZOOM_ACCOUNT_ID  = os.getenv("ZOOM_ACCOUNT_ID", "")
    ZOOM_CLIENT_ID   = os.getenv("ZOOM_CLIENT_ID", "")
    ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET", "")
    ZOOM_TIMEZONE = os.getenv("ZOOM_TIMEZONE", "UTC")
    ZOOM_MEETING_DURATION_MINUTES = int(
        os.getenv("ZOOM_MEETING_DURATION_MINUTES", "60")
    )

    # Mail — loaded from .env so credentials are never hardcoded
    MAIL_SERVER         = os.getenv("MAIL_SERVER",         "smtp.gmail.com")
    MAIL_PORT           = int(os.getenv("MAIL_PORT",       "587"))
    MAIL_USE_TLS        = os.getenv("MAIL_USE_TLS",        "true").lower()  == "true"
    MAIL_USE_SSL        = os.getenv("MAIL_USE_SSL",        "false").lower() == "true"
    MAIL_USERNAME       = os.getenv("MAIL_USERNAME",       "")
    MAIL_PASSWORD       = os.getenv("MAIL_PASSWORD",       "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME", ""))