from app.database.db import db
from app.models.interview import Interview
from app.models.job import Job
from app.models.candidate import Candidate
from app.services.email_service import EmailService
from app.services.zoom_meeting_service import ZoomMeetingService


class InterviewManagementService:

    # ==========================================
    # Get All Interviews
    # ==========================================
    @staticmethod
    def get_all(search="", status=""):

        query = Interview.query

        if search:
            query = query.filter(
                Interview.interviewer.ilike(f"%{search}%")
            )

        if status:
            query = query.filter_by(status=status)

        return query.order_by(
            Interview.interview_date.desc()
        ).all()

    # ==========================================
    # Get Interview
    # ==========================================
    @staticmethod
    def get(interview_id):

        return db.session.get(Interview, interview_id)

    # ==========================================
    # Add Interview
    # ==========================================
    @staticmethod
    def add(
        candidate_id,
        job_id,
        interview_date,
        interview_time,
        interview_mode,
        interviewer,
        meeting_link
    ):

        candidate = db.session.get(Candidate, int(candidate_id))
        job = db.session.get(Job, int(job_id))
        if not candidate or not job:
            return None

        if interview_mode == "Online":
            meeting_link = ZoomMeetingService.create_meeting(
                f"Interview: {job.title}", interview_date, interview_time
            )
        else:
            meeting_link = job.location or "Company Office"

        interview = Interview(

            candidate_id=candidate_id,
            job_id=job_id,
            interview_date=interview_date,
            interview_time=interview_time,
            mode=interview_mode,
            interviewer=interviewer,
            meeting_link=meeting_link,
            status="Scheduled"

        )

        db.session.add(interview)
        db.session.commit()
        if candidate.email:

            EmailService.send_interview_scheduled_email(

                candidate_email=candidate.email,

                candidate_name=candidate.full_name,

                job_title=job.title if job else "Job Position",

                interviewer=interviewer,

                interview_date=interview_date,

                interview_time=interview_time,

                mode=interview_mode,

                meeting_link=interview.meeting_link

            )

        return interview

    # ==========================================
    # Update Interview
    # ==========================================
    @staticmethod
    def update(

        interview_id,
        interview_date,
        interview_time,
        interview_mode,
        interviewer,
        meeting_link,
        status

    ):

        interview = Interview.query.get(interview_id)

        if not interview:
            return None

        previous_mode = interview.mode
        if interview_mode == "Online":
            if previous_mode != "Online" or not (interview.meeting_link or "").startswith("https://zoom.us/"):
                job = db.session.get(Job, interview.job_id)
                interview.meeting_link = ZoomMeetingService.create_meeting(
                    f"Interview: {job.title if job else 'Candidate interview'}",
                    interview_date,
                    interview_time,
                )

        else:
            job = db.session.get(Job, interview.job_id)
            interview.meeting_link = job.location if job and job.location else "Company Office"

        interview.interview_date = interview_date
        interview.interview_time = interview_time
        interview.mode = interview_mode
        interview.interviewer = interviewer
        interview.status = status

        db.session.commit()

        return interview

    # ==========================================
    # Update Status
    # ==========================================
    @staticmethod
    def update_status(interview_id, status):

        interview = Interview.query.get(interview_id)

        if interview:

            interview.status = status

            db.session.commit()

        return interview

    # ==========================================
    # Toggle Status
    # ==========================================
    @staticmethod
    def toggle_status(interview_id):

        interview = Interview.query.get(interview_id)

        if not interview:
            return None

        if interview.status == "Scheduled":

            interview.status = "Completed"

        elif interview.status == "Completed":

            interview.status = "Selected"

        elif interview.status == "Selected":

            interview.status = "Rejected"

        else:

            interview.status = "Scheduled"

        db.session.commit()

        return interview

    # ==========================================
    # Delete Interview
    # ==========================================
    @staticmethod
    def delete(interview_id):

        interview = Interview.query.get(interview_id)

        if interview:

            db.session.delete(interview)

            db.session.commit()