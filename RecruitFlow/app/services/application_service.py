from app.database.db import db
from app.models.application import Application


class ApplicationService:

    # ------------------------------------
    # Apply for Job
    # ------------------------------------

    @staticmethod
    def apply(candidate_id, job_id):

        existing = Application.query.filter_by(
            candidate_id=candidate_id,
            job_id=job_id
        ).first()

        if existing:
            return None

        application = Application(
            candidate_id=candidate_id,
            job_id=job_id,
            status="Applied"
        )

        db.session.add(application)
        db.session.commit()

        return application

    # ------------------------------------
    # Get Candidate Applications
    # ------------------------------------

    @staticmethod
    def get_candidate_applications(candidate_id):

        return Application.query.filter_by(
            candidate_id=candidate_id
        ).all()

    # ------------------------------------
    # Get All Applications
    # ------------------------------------

    @staticmethod
    def get_all():

        return Application.query.order_by(
            Application.application_id.desc()
        ).all()

    # ------------------------------------
    # Get Single Application
    # ------------------------------------

    @staticmethod
    def get(application_id):

        return db.session.get(Application, application_id)

    # ------------------------------------
    # Update Status
    # ------------------------------------

    @staticmethod
    def update_status(application_id, status, remarks=None):

        application = db.session.get(Application, application_id)

        if not application:
            return None

        application.status = status
        application.remarks = remarks

        db.session.commit()

        return application

    # ------------------------------------
    # Delete Application
    # ------------------------------------

    @staticmethod
    def delete(application_id):

        application = db.session.get(Application, application_id)

        if application:

            db.session.delete(application)
            db.session.commit()

            return True

        return False