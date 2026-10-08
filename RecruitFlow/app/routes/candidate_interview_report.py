from flask import Blueprint, Response, request, session, redirect, url_for
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.services.ai_interview_service import AIInterviewService
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from app.database.db import db

candidate_interview_report_bp = Blueprint("candidate_interview_report", __name__)


@candidate_interview_report_bp.route("/candidate/interview-report/<int:interview_id>")
def export_report(interview_id):
    if "candidate_id" not in session:
        return redirect(url_for("candidate_auth.login"))

    interview = Interview.query.filter_by(candidate_id=session["candidate_id"], interview_id=interview_id).first()
    if interview is None:
        return redirect(url_for("candidate_interview.interviews"))

    candidate = db.session.get(Candidate, session["candidate_id"])
    questions = AIInterviewService.generate_for_interview(candidate, interview.job)
    payload = AIInterviewService.build_interview_report_payload(
        candidate=candidate,
        job=interview.job,
        questions=questions,
        transcript=request.args.get("transcript", ""),
        recommendation=request.args.get("recommendation", "Maybe"),
        emotion=request.args.get("emotion", "neutral"),
        eye_contact=request.args.get("eye_contact", "unknown"),
        timer_seconds=int(request.args.get("timer_seconds", 0) or 0),
    )

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setTitle(f"Interview Report - {payload['candidate_name']}")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 780, f"Interview Report - {payload['candidate_name']}")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, 750, f"Job: {payload['job_title']}")
    pdf.drawString(50, 732, f"Recommendation: {payload['recommendation']}")
    pdf.drawString(50, 714, f"Emotion: {payload['emotion']}")
    pdf.drawString(50, 696, f"Eye Contact: {payload['eye_contact']}")
    pdf.drawString(50, 678, f"Timer: {payload['timer_seconds']} seconds")
    pdf.drawString(50, 660, "Summary:")
    pdf.setFont("Helvetica", 10)
    text = pdf.beginText(50, 640)
    for line in payload['summary'].splitlines() or [payload['summary']]:
        text.textLine(line[:110])
    pdf.drawText(text)

    y = 600
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Questions")
    pdf.setFont("Helvetica", 10)
    y -= 18
    for section, items in payload['questions'].items():
        if section == 'evaluation':
            continue
        pdf.drawString(50, y, f"{section.replace('_', ' ').title()}:")
        y -= 14
        for item in items:
            if y < 80:
                pdf.showPage()
                y = 780
                pdf.setFont("Helvetica", 10)
            pdf.drawString(70, y, item[:110])
            y -= 14

    pdf.save()
    buffer.seek(0)
    return Response(buffer.getvalue(), mimetype="application/pdf", headers={"Content-Disposition": f"attachment; filename=interview_report_{interview_id}.pdf"})