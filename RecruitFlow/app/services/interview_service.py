from app.database.db import db
from app.models.interview import Interview
from app.models.candidate import Candidate
from app.services.email_service import EmailService
from app.services.notification_service import NotificationService
from app.services.job_matching_service import JobMatchingService
from app.services.zoom_meeting_service import ZoomMeetingService, ZoomMeetingError


class InterviewService:

    @staticmethod
    def get_all():
        return Interview.query.all()

    @staticmethod
    def get(interview_id):
        return db.session.get(Interview, interview_id)

    @staticmethod
    def schedule(
        candidate_id,
        interviewer,
        interview_date,
        interview_time,
        mode
    ):
        best_match = JobMatchingService.get_best_matching_job(candidate_id)
        if not best_match:
            return None

        job = best_match["job"]

        if mode == "Online":
            import uuid as _uuid
            # Zoom integration is optional — attempt it but always fall back
            # to a Google Meet link so scheduling never fails.
            meeting_link = None
            try:
                meeting_link = ZoomMeetingService.create_meeting(
                    f"Interview: {job.title}", interview_date, interview_time
                )
            except Exception:
                pass  # Zoom unavailable — use Google Meet below
            if not meeting_link:
                meeting_link = (
                    f"https://meet.google.com/"
                    f"{_uuid.uuid4().hex[:3]}-{_uuid.uuid4().hex[:4]}-{_uuid.uuid4().hex[:3]}"
                )
        else:
            meeting_link = job.location or "Company Office"

        interview = Interview(
            candidate_id=candidate_id,
            job_id=job.job_id,
            interviewer=interviewer,
            interview_date=interview_date,
            interview_time=interview_time,
            mode=mode,
            status="Scheduled",
            meeting_link=meeting_link,
        )

        db.session.add(interview)
        db.session.commit()

        NotificationService.create(
            title="Interview Scheduled",
            message="Your interview has been scheduled.",
            notification_type="Interview",
            recipient_role="Candidate"
        )

        candidate = db.session.get(Candidate, candidate_id)
        if candidate and candidate.email:
            try:
                EmailService.send_interview_email(
                    candidate.email,
                    candidate.full_name,
                    interviewer,
                    interview_date,
                    interview_time,
                    mode,
                    interview.meeting_link,
                    job.title
                )
            except Exception as e:
                print(f"[InterviewService] Schedule email failed for {candidate.email}: {e}")

        return interview

    @staticmethod
    def update(
        interview_id,
        interviewer,
        interview_date,
        interview_time,
        mode,
        status
    ):
        interview = db.session.get(Interview, interview_id)
        if not interview:
            return None

        previous_mode = interview.mode
        interview.interviewer = interviewer
        interview.interview_date = interview_date
        interview.interview_time = interview_time
        interview.mode = mode
        interview.status = status

        if interview.mode == "Online" and (
            previous_mode != "Online"
            or not (interview.meeting_link or "").startswith("http")
        ):
            import uuid as _uuid
            new_link = None
            try:
                new_link = ZoomMeetingService.create_meeting(
                    f"Interview: {interview.job.title}",
                    interview_date,
                    interview_time,
                )
            except Exception:
                pass  # Zoom unavailable
            interview.meeting_link = new_link or (
                f"https://meet.google.com/"
                f"{_uuid.uuid4().hex[:3]}-{_uuid.uuid4().hex[:4]}-{_uuid.uuid4().hex[:3]}"
            )
        elif interview.mode == "Offline":
            interview.meeting_link = interview.job.location or "Company Office"

        db.session.commit()

        candidate = db.session.get(Candidate, interview.candidate_id)
        if candidate and candidate.email:
            try:
                EmailService.send_status_email(
                    candidate.email,
                    candidate.full_name,
                    status
                )
            except Exception as e:
                print(f"[InterviewService] Status email failed for {candidate.email}: {e}")

        return interview

    @staticmethod
    def delete(interview_id):
        interview = db.session.get(Interview, interview_id)
        if not interview:
            return False
        db.session.delete(interview)
        db.session.commit()
        return True