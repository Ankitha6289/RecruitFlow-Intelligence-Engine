from app.database.db import db
from app.models.offer import Offer


class RecruiterOfferService:

    @staticmethod
    def get_all():

        return Offer.query.all()


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

            offered_salary=salary,

            status="Pending"

        )

        db.session.add(offer)

        db.session.commit()


    @staticmethod
    def delete(offer_id):

        offer = db.session.get(Offer, offer_id)

        if offer:

            db.session.delete(offer)

            db.session.commit()