from app.database.db import db
from app.models.interview import Interview
from app.models.application import Application
from app.services.email_service import EmailService
from app.services.job_matching_service import JobMatchingService
from app.services.zoom_meeting_service import ZoomMeetingService


class RecruiterInterviewService:

    @staticmethod
    def create(application_id, interviewer, interview_date, interview_time, mode):

        application = db.session.get(Application, application_id)
        if application is None:
            return None

        candidate = application.candidate
        best_match = JobMatchingService.get_best_matching_job(application.candidate_id)
        job = best_match["job"] if best_match else application.job

        if mode == "Online":
            meeting_link = ZoomMeetingService.create_meeting(
                f"Interview: {job.title if job else 'Candidate interview'}",
                interview_date,
                interview_time,
            )
        else:
            meeting_link = job.location if job and job.location else "Company Office"

        # Build interview record (no manual meeting_link submitted)
        interview = Interview(
            candidate_id=application.candidate_id,
            job_id=job.job_id if job else application.job_id,
            interviewer=interviewer,
            interview_date=interview_date,
            interview_time=interview_time,
            mode=mode,
            status="Scheduled",
            meeting_link=meeting_link,
        )

        db.session.add(interview)
        db.session.commit()

        # ── Send confirmation email to candidate ─────────────────────────
        if candidate and candidate.email:
            EmailService.send_interview_scheduled_email(
                candidate_email=candidate.email,
                candidate_name=candidate.full_name,
                job_title=job.title if job else "the position",
                interviewer=interviewer,
                interview_date=interview_date,
                interview_time=interview_time,
                mode=mode,
                meeting_link=interview.meeting_link
            )

        return interview
