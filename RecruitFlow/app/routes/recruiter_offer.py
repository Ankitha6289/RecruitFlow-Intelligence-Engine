from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from app.models.candidate import Candidate
from app.models.job import Job
from app.services.recruiter_offer_service import RecruiterOfferService

recruiter_offer_bp = Blueprint(
    "recruiter_offer",
    __name__
)


@recruiter_offer_bp.route("/recruiter/offers")
def offers():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    offers = RecruiterOfferService.get_all()

    return render_template(
        "recruiter_offers.html",
        offers=offers
    )


@recruiter_offer_bp.route(
    "/recruiter/offers/add",
    methods=["GET", "POST"]
)
def add_offer():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        RecruiterOfferService.create(

            request.form["candidate_id"],

            request.form["job_id"],

            request.form["offer_date"],

            request.form["joining_date"],

            request.form["salary"]

        )

        flash(
            "Offer Generated Successfully.",
            "success"
        )

        return redirect(
            url_for("recruiter_offer.offers")
        )

    candidates = Candidate.query.all()

    jobs = Job.query.all()

    return render_template(

        "recruiter_add_offer.html",

        candidates=candidates,

        jobs=jobs

    )


@recruiter_offer_bp.route(
    "/recruiter/offers/delete/<int:offer_id>"
)
def delete_offer(offer_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    RecruiterOfferService.delete(offer_id)

    flash(
        "Offer Deleted.",
        "danger"
    )

    return redirect(
        url_for("recruiter_offer.offers")
    )