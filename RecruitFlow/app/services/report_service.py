from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

from app.models.candidate import Candidate
from app.models.education import Education
from app.models.skills import Skill
from app.models.experience import Experience
from app.models.ai_analysis import AIAnalysis
from app.database.db import db


class ReportService:

    @staticmethod
    def get_all_candidates(search=""):

        if search:
            return Candidate.query.filter(
                Candidate.full_name.ilike(f"%{search}%")
            ).all()

        return Candidate.query.all()

    @staticmethod
    def generate_candidate_pdf(candidate_id):

        candidate = db.session.get(Candidate, candidate_id)

        if not candidate:
            return None

        education = Education.query.filter_by(
            candidate_id=candidate_id
        ).all()

        skills = Skill.query.filter_by(
            candidate_id=candidate_id
        ).all()

        experience = Experience.query.filter_by(
            candidate_id=candidate_id
        ).all()

        ai = AIAnalysis.query.filter_by(
            candidate_id=candidate_id
        ).first()

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        title = styles["Heading1"]
        title.alignment = TA_CENTER

        story = []

        # Heading

        story.append(
            Paragraph(
                "RecruitFlow Intelligence Engine",
                title
            )
        )

        story.append(
            Paragraph(
                "Candidate Profile Report",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 20))

        # Candidate Information

        data = [

            ["Field", "Value"],

            ["Name", candidate.full_name],

            ["Email", candidate.email],

            ["Phone", candidate.phone],

            ["LinkedIn", candidate.linkedin],

            ["GitHub", candidate.github],

            ["Portfolio", candidate.portfolio],

            ["Status", candidate.status]

        ]

        table = Table(data, colWidths=[150, 320])

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("BACKGROUND",(0,1),(0,-1),colors.lightgrey),

                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

                ("BOTTOMPADDING",(0,0),(-1,0),10),

            ])

        )

        story.append(table)

        story.append(Spacer(1,20))

        # Education

        story.append(
            Paragraph("Education", styles["Heading2"])
        )

        if education:

            for edu in education:

                story.append(
                    Paragraph(
                        f"• {edu.degree}",
                        styles["Normal"]
                    )
                )

        else:

            story.append(
                Paragraph(
                    "No Education Found",
                    styles["Normal"]
                )
            )

        story.append(Spacer(1,15))

        # Skills

        story.append(
            Paragraph("Skills", styles["Heading2"])
        )

        if skills:

            story.append(
                Paragraph(
                    ", ".join(
                        [s.skill_name for s in skills]
                    ),
                    styles["Normal"]
                )
            )

        else:

            story.append(
                Paragraph(
                    "No Skills Found",
                    styles["Normal"]
                )
            )

        story.append(Spacer(1,15))

        # Experience

        story.append(
            Paragraph(
                "Experience",
                styles["Heading2"]
            )
        )

        if experience:

            for exp in experience:

                story.append(
                    Paragraph(
                        f"• {exp.company}",
                        styles["Normal"]
                    )
                )

        else:

            story.append(
                Paragraph(
                    "No Experience Found",
                    styles["Normal"]
                )
            )

        story.append(Spacer(1,15))

        # AI Analysis

        story.append(
            Paragraph(
                "AI Resume Analysis",
                styles["Heading2"]
            )
        )

        if ai:

            story.append(
                Paragraph(
                    f"<b>Summary:</b> {ai.summary}",
                    styles["Normal"]
                )
            )

            story.append(
                Paragraph(
                    f"<b>Suitability Score:</b> {ai.suitability_scores}",
                    styles["Normal"]
                )
            )

            story.append(
                Paragraph(
                    f"<b>Recommended Role:</b> {ai.recommended_roles}",
                    styles["Normal"]
                )
            )

        else:

            story.append(
                Paragraph(
                    "AI Analysis Not Available",
                    styles["Normal"]
                )
            )

        story.append(Spacer(1,25))

        story.append(
            Paragraph(
                "<b>Generated by RecruitFlow Intelligence Engine</b>",
                title
            )
        )

        doc.build(story)

        buffer.seek(0)

        return buffer