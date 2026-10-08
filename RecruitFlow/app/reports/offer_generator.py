from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os


class OfferGenerator:

    @staticmethod
    def generate_pdf(offer):

        # Create folder inside app/generated_offers
        base_dir = os.path.dirname(os.path.dirname(__file__))
        folder = os.path.join(base_dir, "generated_offers")
        os.makedirs(folder, exist_ok=True)

        filename = f"offer_{offer.offer_id}.pdf"
        filepath = os.path.join(folder, filename)

        doc = SimpleDocTemplate(filepath)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "<b><font size=18>RecruitFlow Intelligence Engine</font></b>",
                styles["Title"]
            )
        )

        elements.append(
            Paragraph(
                "<b>Offer Letter</b>",
                styles["Heading1"]
            )
        )

        elements.append(
            Paragraph(
                f"Candidate Name : <b>{offer.candidate.full_name}</b>",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Job Role : <b>{offer.job.title}</b>",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Company : <b>{offer.job.company}</b>",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Salary : <b>{offer.salary}</b>",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Joining Date : <b>{offer.joining_date}</b>",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                "<br/><br/>Congratulations!",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                "We are pleased to offer you this position. "
                "We look forward to having you join our team.",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                "<br/><br/>Regards,<br/><b>HR Team</b><br/>RecruitFlow Intelligence Engine",
                styles["Normal"]
            )
        )

        doc.build(elements)

        return filepath