from io import BytesIO

from flask import send_file
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from app.database.db import db
from app.models.job import Job


class JobManagementService:

    # ==========================================
    # Get All Jobs
    # ==========================================

    @staticmethod
    def get_all(search="", status=""):

        query = Job.query

        if search:
            query = query.filter(
                Job.title.ilike(f"%{search}%")
            )

        if status:
            query = query.filter(
                Job.status == status
            )

        return query.order_by(
            Job.job_id.desc()
        ).all()

    # ==========================================
    # Get Single Job
    # ==========================================

    @staticmethod
    def get(job_id):

        return db.session.get(Job, job_id)

    # ==========================================
    # Add Job
    # ==========================================

    @staticmethod
    def add(
        title,
        company,
        location,
        salary,
        experience,
        skills,
        description
    ):

        job = Job(

            title=title,
            company=company,
            location=location,
            salary=salary,
            experience=experience,
            skills=skills,
            description=description,
            status="Active"

        )

        db.session.add(job)
        db.session.commit()

        return job

    # ==========================================
    # Update Job
    # ==========================================

    @staticmethod
    def update(
        job_id,
        title,
        company,
        location,
        salary,
        experience,
        skills,
        description
    ):

        job = db.session.get(Job, job_id)

        if not job:
            return None

        job.title = title
        job.company = company
        job.location = location
        job.salary = salary
        job.experience = experience
        job.skills = skills
        job.description = description

        db.session.commit()

        return job

    # ==========================================
    # Delete Job
    # ==========================================

    @staticmethod
    def delete(job_id):

        job = db.session.get(Job, job_id)

        if job:

            db.session.delete(job)
            db.session.commit()

    # ==========================================
    # Activate / Close Job
    # ==========================================

    @staticmethod
    def toggle_status(job_id):

        job = db.session.get(Job, job_id)

        if not job:
            return

        if job.status == "Active":
            job.status = "Closed"
        else:
            job.status = "Active"

        db.session.commit()

    # ==========================================
    # Export PDF
    # ==========================================

    @staticmethod
    def export_pdf():

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        rows = [

            ["ID", "Job Title", "Company", "Location", "Status"]

        ]

        jobs = Job.query.order_by(Job.job_id.desc()).all()

        for job in jobs:

            rows.append([

                job.job_id,
                job.title,
                job.company,
                job.location,
                job.status

            ])

        table = Table(rows)

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige)

            ])

        )

        doc.build([table])

        buffer.seek(0)

        return send_file(

            buffer,
            download_name="Jobs.pdf",
            as_attachment=True,
            mimetype="application/pdf"

        )

    # ==========================================
    # Export Excel
    # ==========================================

    @staticmethod
    def export_excel():

        workbook = Workbook()

        sheet = workbook.active

        sheet.title = "Jobs"

        sheet.append([

            "ID",
            "Job Title",
            "Company",
            "Location",
            "Salary",
            "Experience",
            "Status"

        ])

        jobs = Job.query.order_by(Job.job_id.desc()).all()

        for job in jobs:

            sheet.append([

                job.job_id,
                job.title,
                job.company,
                job.location,
                job.salary,
                job.experience,
                job.status

            ])

        output = BytesIO()

        workbook.save(output)

        output.seek(0)

        return send_file(

            output,
            download_name="Jobs.xlsx",
            as_attachment=True,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        )