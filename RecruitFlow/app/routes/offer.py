from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_file
)

from app.models.candidate import Candidate
from app.models.job import Job

from app.services.offer_service import OfferService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService

offer_bp = Blueprint(
    "offer",
    __name__
)


# ======================================================
# View Offers
# ======================================================

@offer_bp.route("/offers")
def offers():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    offers = OfferService.get_all()

    return render_template(
        "offers.html",
        offers=offers
    )


# ======================================================
# Generate Offer
# ======================================================

@offer_bp.route(
    "/offers/add",
    methods=["GET", "POST"]
)
def add_offer():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        OfferService.create(

            request.form["candidate_id"],

            request.form["job_id"],

            request.form["offer_date"],

            request.form["joining_date"],

            request.form["salary"]

        )

        # -------------------------
        # Activity Log
        # -------------------------

        ActivityLogService.create(

            session["user_id"],

            "Generated Offer Letter",

            "Offers"

        )

        # -------------------------
        # Notification
        # -------------------------

        NotificationService.create(

            title="Offer Letter Generated",

            message="A new offer letter has been generated.",

            notification_type="Offers",

            recipient_role="Recruiter"

        )

        flash(
            "Offer Generated Successfully",
            "success"
        )

        return redirect(
            url_for("offer.offers")
        )

    candidates = Candidate.query.all()

    jobs = Job.query.all()

    return render_template(
        "add_offer.html",
        candidates=candidates,
        jobs=jobs
    )
# ======================================================
# Edit Offer
# ======================================================

@offer_bp.route(
    "/offers/edit/<int:offer_id>",
    methods=["GET", "POST"]
)
def edit_offer(offer_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    offer = OfferService.get(offer_id)

    if offer is None:

        flash(
            "Offer Not Found",
            "danger"
        )

        return redirect(
            url_for("offer.offers")
        )

    if request.method == "POST":

        OfferService.update(

            offer_id,

            request.form["offer_date"],

            request.form["joining_date"],

            request.form["salary"],

            request.form["status"]

        )

        # ----------------------------------
        # Activity Log
        # ----------------------------------

        ActivityLogService.create(

            session["user_id"],

            "Updated Offer Letter",

            "Offers"

        )

        # ----------------------------------
        # Notification
        # ----------------------------------

        NotificationService.create(

            title="Offer Updated",

            message="Offer letter updated successfully.",

            notification_type="Offers",

            recipient_role="Recruiter"

        )

        flash(

            "Offer Updated Successfully",

            "success"

        )

        return redirect(
            url_for("offer.offers")
        )

    return render_template(

        "edit_offer.html",

        offer=offer

    )
# ======================================================
# Update Offer Status
# ======================================================

@offer_bp.route("/offers/status/<int:offer_id>/<status>")
def offer_status(offer_id, status):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    OfferService.update_status(
        offer_id,
        status
    )

    # ----------------------------------
    # Accepted
    # ----------------------------------

    if status == "Accepted":

        ActivityLogService.create(

            session["user_id"],

            "Offer Accepted",

            "Offers"

        )

        NotificationService.create(

            title="Offer Accepted",

            message="Candidate accepted the offer.",

            notification_type="Offers",

            recipient_role="Recruiter"

        )

    # ----------------------------------
    # Declined
    # ----------------------------------

    elif status == "Declined":

        ActivityLogService.create(

            session["user_id"],

            "Offer Declined",

            "Offers"

        )

        NotificationService.create(

            title="Offer Declined",

            message="Candidate declined the offer.",

            notification_type="Offers",

            recipient_role="Recruiter"

        )

    # ----------------------------------
    # Other Status
    # ----------------------------------

    else:

        ActivityLogService.create(

            session["user_id"],

            "Offer Status Updated",

            "Offers"

        )

        NotificationService.create(

            title="Offer Updated",

            message="Offer status updated successfully.",

            notification_type="Offers",

            recipient_role="Recruiter"

        )

    flash(
        "Offer Status Updated Successfully",
        "success"
    )

    return redirect(
        url_for("offer.offers")
    )
# ======================================================
# Download Offer PDF
# ======================================================

@offer_bp.route("/offers/pdf/<int:offer_id>")
def download_offer(offer_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    offer = OfferService.get(offer_id)

    if offer is None:

        flash(
            "Offer Not Found",
            "danger"
        )

        return redirect(
            url_for("offer.offers")
        )

    # ----------------------------------
    # Activity Log
    # ----------------------------------

    ActivityLogService.create(

        session["user_id"],

        "Downloaded Offer Letter",

        "Offers"

    )

    # ----------------------------------
    # Notification
    # ----------------------------------

    NotificationService.create(

        title="Offer Downloaded",

        message="Offer letter PDF downloaded.",

        notification_type="Offers",

        recipient_role="Recruiter"

    )

    return send_file(

        offer.pdf_path,

        as_attachment=True

    )


# ======================================================
# Delete Offer
# ======================================================

@offer_bp.route("/offers/delete/<int:offer_id>")
def delete_offer(offer_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    offer = OfferService.get(offer_id)

    if offer is None:

        flash(
            "Offer Not Found",
            "danger"
        )

        return redirect(
            url_for("offer.offers")
        )

    OfferService.delete(offer_id)

    # ----------------------------------
    # Activity Log
    # ----------------------------------

    ActivityLogService.create(

        session["user_id"],

        "Deleted Offer Letter",

        "Offers"

    )

    # ----------------------------------
    # Notification
    # ----------------------------------

    NotificationService.create(

        title="Offer Deleted",

        message="Offer letter deleted successfully.",

        notification_type="Offers",

        recipient_role="Recruiter"

    )

    flash(

        "Offer Deleted Successfully",

        "success"

    )

    return redirect(
        url_for("offer.offers")
    )