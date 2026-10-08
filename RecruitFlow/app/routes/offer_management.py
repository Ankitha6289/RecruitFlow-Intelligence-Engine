from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app.services.offer_management_service import OfferManagementService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService
from app.models.candidate import Candidate
from app.models.job import Job
from flask import send_file

from app.services.offer_report_service import OfferReportService
from app.services.offer_email_service import OfferEmailService
offer_management_bp = Blueprint(
    "offer_management",
    __name__
)


# =====================================================
# View Offers
# =====================================================

@offer_management_bp.route("/admin/offers")
def offers():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    offers = OfferManagementService.get_all()

    return render_template(
        "offers.html",
        offers=offers
    )


# =====================================================
# Create Offer
# =====================================================

@offer_management_bp.route(
    "/admin/offers/add",
    methods=["GET", "POST"]
)
def add_offer():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        offer = OfferManagementService.add(

            request.form["candidate_id"],

            request.form["job_id"],

            request.form["offered_salary"],

            request.form["joining_date"],

            request.form["offer_date"]

        )

        ActivityLogService.create(

            session["user_id"],

            "Offer Created",

            "Offer Management"

        )

        NotificationService.create(

            title="Offer Created",

            message="Offer Letter Generated Successfully.",

            notification_type="Offer",

            recipient_role="Admin"

        )

        # Auto-send offer email with PDF attachment
        try:
            OfferEmailService.send_offer(offer.candidate, offer)
            flash("Offer Created & Email Sent to Candidate.", "success")
        except Exception as e:
            flash(f"Offer Created. Email failed: {e}", "warning")

        return redirect(
            url_for("offer_management.offers")
        )

    candidates = Candidate.query.all()
    jobs = Job.query.all()

    return render_template(
        "add_offer.html",
        candidates=candidates,
        jobs=jobs
    )
# =====================================================
# Accept Offer
# =====================================================

@offer_management_bp.route(
    "/admin/offers/accept/<int:offer_id>"
)
def accept_offer(offer_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    OfferManagementService.update_status(

        offer_id,

        "Accepted"

    )

    ActivityLogService.create(

        session["user_id"],

        "Offer Accepted",

        "Offer Management"

    )

    NotificationService.create(

        title="Offer Accepted",

        message="Candidate accepted the offer.",

        notification_type="Offer",

        recipient_role="Admin"

    )

    flash(

        "Offer Accepted.",

        "success"

    )

    return redirect(
        url_for("offer_management.offers")
    )


# =====================================================
# Reject Offer
# =====================================================

@offer_management_bp.route(
    "/admin/offers/reject/<int:offer_id>"
)
def reject_offer(offer_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    OfferManagementService.update_status(

        offer_id,

        "Rejected"

    )

    ActivityLogService.create(

        session["user_id"],

        "Offer Rejected",

        "Offer Management"

    )

    NotificationService.create(

        title="Offer Rejected",

        message="Candidate rejected the offer.",

        notification_type="Offer",

        recipient_role="Admin"

    )

    flash(

        "Offer Rejected.",

        "warning"

    )

    return redirect(
        url_for("offer_management.offers")
    )

# =====================================================
# Edit Offer
# =====================================================
@offer_management_bp.route(
    "/admin/offers/edit/<int:offer_id>",
    methods=["GET", "POST"]
)
def edit_offer(offer_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    offer = OfferManagementService.get(offer_id)

    if offer is None:

        flash(
            "Offer Not Found.",
            "danger"
        )

        return redirect(
            url_for("offer_management.offers")
        )

    if request.method == "POST":

        OfferManagementService.update(

    offer_id,

    request.form["offered_salary"],

    request.form["joining_date"],

    request.form["offer_date"],

    request.form["status"]

)

        ActivityLogService.create(

            session["user_id"],

            "Updated Offer",

            "Offer Management"

        )

        NotificationService.create(

            title="Offer Updated",

            message="Offer updated successfully.",

            notification_type="Offer",

            recipient_role="Admin"

        )

        flash(
            "Offer Updated Successfully.",
            "success"
        )

        return redirect(
            url_for("offer_management.offers")
        )

    return render_template(
        "edit_offer.html",
        offer=offer
    )
# =====================================================
# Download Offer PDF
# =====================================================

@offer_management_bp.route(
    "/admin/offers/pdf/<int:offer_id>"
)
def download_offer(offer_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    pdf = OfferReportService.generate_offer_pdf(offer_id)

    if pdf is None:
        return "Offer Not Found"

    return send_file(

        pdf,

        download_name=f"Offer_{offer_id}.pdf",

        as_attachment=True,

        mimetype="application/pdf"

    )
# =====================================================
# Send Offer Email
# =====================================================

@offer_management_bp.route(
    "/admin/offers/email/<int:offer_id>"
)
def send_offer_email(offer_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    offer = OfferManagementService.get(offer_id)

    if offer is None:

        flash(

            "Offer Not Found.",

            "danger"

        )

        return redirect(
            url_for("offer_management.offers")
        )

    OfferEmailService.send_offer(

        offer.candidate,

        offer

    )

    ActivityLogService.create(

        session["user_id"],

        "Offer Email Sent",

        "Offer Management"

    )

    NotificationService.create(

        title="Offer Email",

        message=f"Offer email sent to {offer.candidate.full_name}.",

        notification_type="Offer",

        recipient_role="Admin"

    )

    flash(

        "Offer Email Sent Successfully.",

        "success"

    )

    return redirect(
        url_for("offer_management.offers")
    )
# =====================================================
# Delete Offer
# =====================================================

@offer_management_bp.route(
    "/admin/offers/delete/<int:offer_id>"
)
def delete_offer(offer_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    OfferManagementService.delete(offer_id)

    ActivityLogService.create(

        session["user_id"],

        "Offer Deleted",

        "Offer Management"

    )

    NotificationService.create(

        title="Offer Deleted",

        message="Offer deleted successfully.",

        notification_type="Offer",

        recipient_role="Admin"

    )

    flash(

        "Offer Deleted Successfully.",

        "success"

    )

    return redirect(
        url_for("offer_management.offers")
    )