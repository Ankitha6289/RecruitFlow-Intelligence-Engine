from app.database.db import db
from app.models.offer import Offer
from app.models.candidate import Candidate
from app.models.job import Job
from app.reports.offer_generator import OfferGenerator
from app.services.email_service import EmailService
from app.services.notification_service import NotificationService


class OfferService:

    # ==========================================
    # Get All Offers
    # ==========================================
    @staticmethod
    def get_all():

        return Offer.query.all()

    # ==========================================
    # Get Single Offer
    # ==========================================
    @staticmethod
    def get(offer_id):

        return db.session.get(Offer, offer_id)

    # ==========================================
    # Create Offer
    # ==========================================
    @staticmethod
    def create(
        candidate_id,
        job_id,
        offer_date,
        joining_date,
        salary
    ):

        offer = Offer(

            candidate_id=candidate_id,

            job_id=job_id,

            offer_date=offer_date,

            joining_date=joining_date,

            salary=salary,

            status="Pending"

        )

        db.session.add(offer)
        db.session.commit()

        NotificationService.create(

            title="Offer Letter Generated",

            message="A new offer letter has been generated.",

            notification_type="Offer",

            recipient_role="Candidate"

        )

        # Generate PDF
        pdf_path = OfferGenerator.generate_pdf(offer)

        offer.pdf_path = pdf_path

        db.session.commit()

        candidate = db.session.get(Candidate, candidate_id)

        job = db.session.get(Job, job_id)

        EmailService.offer_email(candidate)

        return offer

    # ==========================================
    # Update Offer
    # ==========================================
    @staticmethod
    def update(

        offer_id,

        offer_date,

        joining_date,

        salary,

        status

    ):

        offer = db.session.get(Offer, offer_id)

        if offer is None:
            return None

        offer.offer_date = offer_date
        offer.joining_date = joining_date
        offer.salary = salary
        offer.status = status

        db.session.commit()

        return offer

    # ==========================================
    # Update Status
    # ==========================================
    @staticmethod
    def update_status(
        offer_id,
        status
    ):

        offer = db.session.get(Offer, offer_id)

        if offer:

            offer.status = status

            db.session.commit()

    # ==========================================
    # Delete Offer
    # ==========================================
    @staticmethod
    def delete(offer_id):

        offer = db.session.get(Offer, offer_id)

        if offer:

            db.session.delete(offer)

            db.session.commit()