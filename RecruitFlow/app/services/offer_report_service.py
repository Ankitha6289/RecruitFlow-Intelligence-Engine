from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

from app.models.offer import Offer
from app.database.db import db


class OfferReportService:

    @staticmethod
    def generate_offer_pdf(offer_id):

        offer = db.session.get(Offer, offer_id)

        if not offer:
            return None

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        title = styles["Heading1"]
        title.alignment = TA_CENTER

        story = []

        story.append(
            Paragraph(
                "RecruitFlow Intelligence Engine",
                title
            )
        )

        story.append(
            Paragraph(
                "Offer Letter",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                f"<b>Candidate:</b> {offer.candidate.full_name}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Job Title:</b> {offer.job.title}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Company:</b> {offer.job.company}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Offer Date:</b> {offer.offer_date}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Joining Date:</b> {offer.joining_date}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Salary:</b> {offer.salary}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "Congratulations! We are pleased to offer you this position. "
                "We look forward to welcoming you to our organization.",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 30))

        story.append(
            Paragraph(
                "<b>RecruitFlow HR Team</b>",
                styles["Heading3"]
            )
        )

        doc.build(story)

        buffer.seek(0)

        return buffer