from app.database.db import db
from app.models.offer import Offer


class OfferManagementService:

    # ==========================================
    # Get All Offers
    # ==========================================

    @staticmethod
    def get_all():

        return Offer.query.order_by(
            Offer.offer_id.desc()
        ).all()

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
    def add(

        candidate_id,

        job_id,

        salary,

        joining_date,

        offer_date

    ):

        offer = Offer(

            candidate_id=candidate_id,

            job_id=job_id,

            salary=salary,

            joining_date=joining_date,

            offer_date=offer_date,

            status="Pending"

        )

        db.session.add(offer)

        db.session.commit()

        return offer

    # ==========================================
    # Update Offer
    # ==========================================
    @staticmethod
    def update(
        offer_id,
        salary,
        joining_date,
        offer_date,
        status
    ):

        offer = db.session.get(Offer, offer_id)

        if offer is None:
            return None

        offer.salary = salary
        offer.joining_date = joining_date
        offer.offer_date = offer_date
        offer.status = status

        db.session.commit()

        return offer
    # ==========================================
    # Update Offer Status
    # ==========================================
    @staticmethod
    def update_status(offer_id, status):

        offer = db.session.get(Offer, offer_id)

        if offer is None:
            return None

        offer.status = status

        db.session.commit()

        return offer

    # ==========================================
    # Delete Offer
    # ==========================================

    @staticmethod
    def delete(offer_id):

        offer = db.session.get(Offer, offer_id)

        if offer:

            db.session.delete(offer)

            db.session.commit()