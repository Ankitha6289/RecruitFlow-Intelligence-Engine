from flask import Flask
from flask_migrate import Migrate

from config import Config
from app.database.db import db
from app.extensions import mail

migrate = Migrate()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    db.init_app(app)

    migrate.init_app(app, db)

    mail.init_app(app)

    # Import models
    from app.models.candidate import Candidate
    from app.models.education import Education
    from app.models.experience import Experience
    from app.models.skills import Skill
    from app.models.ai_analysis import AIAnalysis
    from app.models.user import User
    from app.models.interview import Interview
    from app.models.interview_proctor_event import InterviewProctorEvent
    from app.models.job import Job
    from app.models.offer import Offer
    from app.models.ats_analysis import ATSAnalysis
    from app.models.skill_gap import SkillGap
    from app.models.interview_questions import InterviewQuestion
    from app.models.chatbot_history import ChatbotHistory
    from app.models.application import Application
    from app.models.notification import Notification
    from app.models.activity_log import ActivityLog
    from app.models.job_match import JobMatch
    from app.models.settings import Settings
    
    
    # Register Blueprints
    from app.routes.upload import upload_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.search import search_bp
    from app.routes.profile import profile_bp
    from app.routes.report import report_bp
    from app.routes.excel import excel_bp
    from app.routes.auth import auth_bp
    from app.routes.recruiter import recruiter_bp
    from app.routes.recruiter_dashboard import recruiter_dashboard_bp
    from app.routes.interview import interview_bp
    from app.routes.job import job_bp
    from app.routes.job_matching import match_bp
    from app.routes.ranking import ranking_bp
    from app.routes.candidate_status import status_bp
    from app.routes.offer import offer_bp
  
    from app.routes.settings import settings_bp
    from app.routes.recruiter_profile import recruiter_profile_bp
    from app.routes.notification import notification_bp
    from app.routes.activity_log import activity_log_bp
    from app.routes.chatbot import chatbot_bp
    from app.routes.ats import ats_bp
    from app.routes.skill_gap import skill_gap_bp
    from app.routes.ai_interview import ai_interview_bp
    from app.routes.candidate_auth import candidate_auth_bp
    from app.routes.candidate_dashboard import candidate_dashboard_bp
    from app.routes.candidate_profile import candidate_profile_bp
    from app.routes.application_routes import application_bp
    from app.routes.analytics import analytics_bp
    
    from app.routes.admin_dashboard import admin_dashboard_bp
    from app.routes.admin_profile import admin_profile_bp
    from app.routes.user_management import user_management_bp
    from app.routes.change_password import change_password_bp
    from app.routes.backup import backup_bp
    from app.routes.recruiter_job import recruiter_job_bp
    from app.routes.recruiter_application import recruiter_application_bp
    from app.routes.recruiter_interview import recruiter_interview_bp
    from app.routes.recruiter_interview_list import recruiter_interview_list_bp
    from app.routes.recruiter_offer import recruiter_offer_bp
    from app.routes.offer_management import offer_management_bp
    from app.routes.candidate_resume import candidate_resume_bp
    from app.routes.file_route import file_bp
    from app.routes.candidate_jobs import candidate_jobs_bp
    from app.routes.candidate_applications import candidate_application_bp
    from app.routes.candidate_interviews import candidate_interview_bp
    from app.routes.candidate_interview_report import candidate_interview_report_bp
    from app.routes.candidate_offers import candidate_offer_bp
    from app.routes.candidate_notifications import candidate_notification_bp
    from app.routes.candidate_settings import candidate_settings_bp
    from app.routes.admin_analytics import admin_analytics_bp
    from app.controllers.reports_controller import reports_bp
    from app.controllers.report_export_controller import report_export_bp
    from app.controllers.job_management_controller import job_management_bp
    from app.controllers.candidate_management_controller import candidate_management_bp
    from app.controllers.interview_management_controller import interview_management_bp
    from app.routes.offer_management import offer_management_bp
    
    app.register_blueprint(upload_bp)
   
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(excel_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(recruiter_bp)

    app.register_blueprint(recruiter_dashboard_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(match_bp)
    app.register_blueprint(ranking_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(offer_bp)
    
    app.register_blueprint(settings_bp)
    app.register_blueprint(recruiter_profile_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(activity_log_bp)
    app.register_blueprint(ats_bp)
    app.register_blueprint(skill_gap_bp)
    app.register_blueprint(ai_interview_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(candidate_auth_bp)
    app.register_blueprint(candidate_dashboard_bp)
    app.register_blueprint(candidate_profile_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(analytics_bp)
    
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(admin_profile_bp)
    app.register_blueprint(user_management_bp)
    app.register_blueprint(change_password_bp)
    app.register_blueprint(backup_bp)
    app.register_blueprint(job_management_bp)
    app.register_blueprint(recruiter_job_bp)
    app.register_blueprint(recruiter_application_bp)
    app.register_blueprint(recruiter_interview_bp)
    app.register_blueprint(recruiter_interview_list_bp)
    app.register_blueprint(recruiter_offer_bp)
    app.register_blueprint(candidate_resume_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(candidate_jobs_bp)
    app.register_blueprint(candidate_application_bp)
    app.register_blueprint(candidate_interview_bp)
    app.register_blueprint(candidate_interview_report_bp)
    app.register_blueprint(candidate_offer_bp)
    app.register_blueprint(candidate_notification_bp)
    app.register_blueprint(candidate_settings_bp)
    app.register_blueprint(admin_analytics_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(report_export_bp)
    app.register_blueprint(candidate_management_bp)
    app.register_blueprint(interview_management_bp)
    app.register_blueprint(offer_management_bp)
    
    return app