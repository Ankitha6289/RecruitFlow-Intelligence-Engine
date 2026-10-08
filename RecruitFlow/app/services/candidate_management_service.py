from io import BytesIO

from flask import send_file
from openpyxl import Workbook

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle
)

from app.database.db import db
from app.models.candidate import Candidate
from app.models.ai_analysis import AIAnalysis


class CandidateManagementService:

    @staticmethod
    def build_scoring_dashboard_data(candidates):
        scored_candidates = []

        for candidate in candidates:
            ai_score = 0
            ats_score = 0

            if candidate.analysis:
                try:
                    ai_score = float(candidate.analysis[0].suitability_scores or 0)
                except (ValueError, TypeError):
                    ai_score = 0

            if getattr(candidate, "ats_analysis", None):
                try:
                    ats_score = float(candidate.ats_analysis[0].ats_score or 0)
                except (ValueError, TypeError):
                    ats_score = 0

            overall_score = round((ai_score + ats_score) / 2, 2)

            scored_candidates.append({
                "candidate": candidate,
                "ai_score": ai_score,
                "ats_score": ats_score,
                "overall_score": overall_score,
            })

        scored_candidates.sort(key=lambda item: item["overall_score"], reverse=True)

        return {
            "total_candidates": len(scored_candidates),
            "average_score": round(
                sum(item["overall_score"] for item in scored_candidates) / len(scored_candidates), 2
            ) if scored_candidates else 0,
            "top_candidates": scored_candidates[:10],
        }

    # ==========================================
    # Get All Candidates
    # ==========================================

    @staticmethod
    def get_all(search="", status="", skill="", min_score=None):

        query = Candidate.query

        if search:

            query = query.filter(
                Candidate.full_name.ilike(f"%{search}%")
            )

        if status:

            query = query.filter_by(
                status=status
            )

        if skill:

            query = query.join(Candidate.skills).filter(
                db.or_(
                    Candidate.skills.any(skill_name=skill),
                    Candidate.skills.any(skill_name=skill.title())
                )
            )

        candidates = query.order_by(
            Candidate.candidate_id.desc()
        ).all()

        if min_score is not None:
            filtered = []
            for candidate in candidates:
                analysis = candidate.analysis[0] if candidate.analysis else None
                score = 0
                if analysis and analysis.suitability_scores:
                    try:
                        score = float(analysis.suitability_scores)
                    except ValueError:
                        score = 0
                if score >= float(min_score):
                    filtered.append(candidate)
            return filtered

        return candidates

    # ==========================================
    # Get Single Candidate
    # ==========================================

    @staticmethod
    def get(candidate_id):

        return db.session.get(Candidate, candidate_id)

    @staticmethod
    def get_score_summary():

        analyses = AIAnalysis.query.all()
        scored = []

        for analysis in analyses:
            try:
                score = float(analysis.suitability_scores or 0)
            except ValueError:
                score = 0
            scored.append(score)

        if not scored:
            return {
                "average": 0,
                "high": 0,
                "low": 0
            }

        return {
            "average": round(sum(scored) / len(scored), 2),
            "high": max(scored),
            "low": min(scored)
        }

    # ==========================================
    # Update Candidate
    # ==========================================

    @staticmethod
    def update(

        candidate_id,

        full_name,

        email,

        phone,

        address,

        linkedin,

        github,

        portfolio,

        status

    ):

        candidate = db.session.get(Candidate, candidate_id)

        if candidate is None:
            return None

        candidate.full_name = full_name
        candidate.email = email
        candidate.phone = phone
        candidate.address = address
        candidate.linkedin = linkedin
        candidate.github = github
        candidate.portfolio = portfolio
        candidate.status = status

        db.session.commit()

        return candidate

    # ==========================================
    # Delete Candidate
    # ==========================================

    @staticmethod
    def delete(candidate_id):

        candidate = db.session.get(Candidate, candidate_id)

        if candidate:

            db.session.delete(candidate)
            db.session.commit()

    # ==========================================
    # Export PDF
    # ==========================================

    @staticmethod
    def export_pdf():

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "Candidate Report",
                styles["Title"]
            )
        )

        rows = [[
            "ID",
            "Name",
            "Email",
            "Phone",
            "Status"
        ]]

        candidates = Candidate.query.all()

        for c in candidates:

            rows.append([
                c.candidate_id,
                c.full_name,
                c.email,
                c.phone,
                c.status
            ])

        table = Table(rows)

        table.setStyle(TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige)

        ]))

        elements.append(table)

        doc.build(elements)

        buffer.seek(0)

        return send_file(

            buffer,

            as_attachment=True,

            download_name="Candidates.pdf",

            mimetype="application/pdf"

        )

    # ==========================================
    # Export Excel
    # ==========================================

    @staticmethod
    def export_excel():

        workbook = Workbook()

        sheet = workbook.active

        sheet.title = "Candidates"

        sheet.append([

            "ID",

            "Name",

            "Email",

            "Phone",

            "Status"

        ])

        candidates = Candidate.query.all()

        for c in candidates:

            sheet.append([

                c.candidate_id,

                c.full_name,

                c.email,

                c.phone,

                c.status

            ])

        output = BytesIO()

        workbook.save(output)

        output.seek(0)

        return send_file(

            output,

            as_attachment=True,

            download_name="Candidates.xlsx",

            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )