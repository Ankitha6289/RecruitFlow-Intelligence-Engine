from app.database.db import db
from app.models.job import Job


class RecruiterJobService:

    # ==========================================
    # Get All Jobs
    # ==========================================

    @staticmethod
    def get_all(user_id, keyword=""):

        query = Job.query.filter_by(
            recruiter_id=user_id
        )

        if keyword:

            query = query.filter(
                Job.title.ilike(
                    f"%{keyword}%"
                )
            )

        return query.order_by(
            Job.created_at.desc()
        ).all()


    # ==========================================
    # Get Single Job
    # ==========================================

    @staticmethod
    def get(job_id):

        return db.session.get(
            Job,
            job_id
        )


    # ==========================================
    # Add Job
    # ==========================================

    @staticmethod
    def add(
        recruiter_id,
        title,
        company,
        location,
        experience,
        salary,
        skills,
        description
    ):

        job = Job(

            recruiter_id=recruiter_id,

            title=title,

            company=company,

            location=location,

            experience=experience,

            salary=salary,

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
        experience,
        salary,
        skills,
        description
    ):

        job = db.session.get(
            Job,
            job_id
        )

        if job is None:
            return None

        job.title = title
        job.company = company
        job.location = location
        job.experience = experience
        job.salary = salary
        job.skills = skills
        job.description = description

        db.session.commit()

        return job


    # ==========================================
    # Delete Job
    # ==========================================

    @staticmethod
    def delete(job_id):

        job = db.session.get(
            Job,
            job_id
        )

        if job:

            db.session.delete(job)

            db.session.commit()

            return True

        return False


    # ==========================================
    # Toggle Job Status
    # ==========================================

    @staticmethod
    def toggle(job_id):

        job = db.session.get(
            Job,
            job_id
        )

        if job is None:
            return None

        if job.status == "Active":

            job.status = "Inactive"

        else:

            job.status = "Active"

        db.session.commit()

        return job