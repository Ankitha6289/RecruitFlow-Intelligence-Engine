from app.database.db import db
from app.models.application import Application


class RecruiterApplicationService:

    @staticmethod
    def get_all():

        return Application.query.all()


    @staticmethod
    def shortlist(application_id):

        application = db.session.get(Application, application_id)

        if application:

            application.status = "Shortlisted"
            application.candidate.status = "Shortlisted"

            db.session.commit()


    @staticmethod
    def reject(application_id):

        application = db.session.get(Application, application_id)

        if application:

            application.status = "Rejected"
            application.candidate.status = "Rejected"

            db.session.commit()