from app.database.db import db
from app.models.candidate import Candidate
from app.services.email_service import EmailService


class CandidateStatusService:


    @staticmethod
    def update_status(candidate_id, status):

        candidate = db.session.get(Candidate, candidate_id)


        if candidate:

            candidate.status = status

            db.session.commit()


            # Send Email Notification

            if status == "Selected":

                EmailService.selection_email(candidate)


            elif status == "Rejected":

                EmailService.rejection_email(candidate)


            elif status in {"Interview", "Technical Interview", "Offer Sent"}:

                EmailService.interview_email(candidate)

            elif status == "Offer Sent":

                EmailService.offer_email(candidate)


            return True


        return False