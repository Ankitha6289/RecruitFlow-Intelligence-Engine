from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash
)

from app.database.db import db
from app.models.offer import Offer

candidate_offer_bp = Blueprint(
    "candidate_offer",
    __name__
)


@candidate_offer_bp.route("/candidate/offers")
def offers():

    if "candidate_id" not in session:
        return redirect(
            url_for("candidate_auth.login")
        )

    offers = Offer.query.filter_by(
        candidate_id=session["candidate_id"]
    ).all()

    return render_template(
        "candidates/offers.html",
        offers=offers
    )


@candidate_offer_bp.route(
    "/candidate/offers/<int:offer_id>/accept"
)
def accept_offer(offer_id):

    if "candidate_id" not in session:
        return redirect(url_for("candidate_auth.login"))

    offer = Offer.query.get_or_404(offer_id)

    if offer.candidate_id != session["candidate_id"]:
        return redirect(
            url_for("candidate_offer.offers")
        )

    offer.status = "Accepted"

    db.session.commit()

    flash(
        "Offer Accepted Successfully.",
        "success"
    )

    return redirect(
        url_for("candidate_offer.offers")
    )


@candidate_offer_bp.route(
    "/candidate/offers/<int:offer_id>/reject"
)
def reject_offer(offer_id):

    if "candidate_id" not in session:
        return redirect(url_for("candidate_auth.login"))

    offer = Offer.query.get_or_404(offer_id)

    if offer.candidate_id != session["candidate_id"]:
        return redirect(
            url_for("candidate_offer.offers")
        )

    offer.status = "Rejected"

    db.session.commit()

    flash(
        "Offer Rejected.",
        "warning"
    )

    return redirect(
        url_for("candidate_offer.offers")
    )