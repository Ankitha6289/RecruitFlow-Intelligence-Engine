from flask_mail import Message
from app.extensions import mail
from app.services.offer_report_service import OfferReportService


class OfferEmailService:

    @staticmethod
    def send_offer(candidate, offer):
        """Send offer email with PDF attachment to candidate."""

        subject = "Your Offer Letter – RecruitFlow"

        body = f"""Dear {candidate.full_name},

Congratulations! We are pleased to extend an offer of employment to you.

────────────────────────────────
  OFFER DETAILS
────────────────────────────────
  Position     : {offer.job.title}
  Company      : {offer.job.company}
  Salary       : {offer.salary}
  Offer Date   : {offer.offer_date}
  Joining Date : {offer.joining_date}
────────────────────────────────

Please find your official offer letter attached to this email.

To accept or decline this offer, please log in to your RecruitFlow portal.

If you have any questions, feel free to reach out to our HR team.

Warm regards,
RecruitFlow HR Team
"""

        msg = Message(subject, recipients=[candidate.email])
        msg.body = body

        # Generate PDF and attach — log but continue if PDF fails
        try:
            pdf_buffer = OfferReportService.generate_offer_pdf(offer.offer_id)
            if pdf_buffer:
                msg.attach(
                    filename=f"Offer_Letter_{candidate.full_name.replace(' ', '_')}.pdf",
                    content_type="application/pdf",
                    data=pdf_buffer.read()
                )
                print(f"[OfferEmailService] PDF attached for offer #{offer.offer_id}")
        except Exception as e:
            print(f"[OfferEmailService] PDF generation/attachment failed for offer #{offer.offer_id}: {e}")

        # Send — re-raise so callers know the email failed
        mail.send(msg)
        print("=" * 50)
        print("OFFER EMAIL SENT")
        print("To      :", candidate.email)
        print("Subject :", subject)
        print("=" * 50)
