import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from app import create_app
from app.database.db import db
from app.models.application import Application
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.skills import Skill
from app.services.interview_management_service import InterviewManagementService
from app.services.interview_service import InterviewService
from app.services.job_matching_service import JobMatchingService
from app.services.recruiter_interview_service import RecruiterInterviewService
from app.services.zoom_meeting_service import ZoomMeetingError, ZoomMeetingService


class InterviewSchedulingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True

    def test_best_job_uses_parsed_resume_skills(self):
        candidate = SimpleNamespace(candidate_id=3)
        python_job = SimpleNamespace(
            job_id=10,
            title="Python Engineer",
            skills="Python, Flask, SQL",
        )
        design_job = SimpleNamespace(
            job_id=11,
            title="UX Designer",
            skills="Figma, Research",
        )

        with self.app.app_context(), \
             patch("app.services.job_matching_service.db.session.get", return_value=candidate), \
             patch.object(Skill, "query") as skill_query, \
             patch.object(Job, "query") as job_query:
            skill_query.filter_by.return_value.all.return_value = [
                SimpleNamespace(skill_name="Python"),
                SimpleNamespace(skill_name="SQL"),
            ]
            job_query.all.return_value = [python_job, design_job]

            result = JobMatchingService.get_best_matching_job(3)

        self.assertEqual(result["job"], python_job)
        self.assertEqual(result["score"], 66.67)

    def test_admin_offline_interview_emails_job_location(self):
        candidate = SimpleNamespace(email="candidate@example.com", full_name="Taylor")
        job = SimpleNamespace(job_id=8, title="Analyst", location="Main Office")

        with self.app.app_context(), \
             patch.object(db.session, "get", side_effect=lambda model, key: candidate if model is Candidate else job), \
             patch.object(db.session, "add"), \
             patch.object(db.session, "commit"), \
             patch("app.services.interview_management_service.EmailService.send_interview_scheduled_email") as send_email, \
             patch("app.services.interview_management_service.ZoomMeetingService.create_meeting") as create_meeting:
            interview = InterviewManagementService.add(
                "3", "8", "2026-10-01", "09:30", "Offline", "Recruiter", ""
            )

        self.assertEqual(interview.job_id, "8")
        self.assertEqual(interview.meeting_link, "Main Office")
        self.assertEqual(send_email.call_args.kwargs["meeting_link"], "Main Office")
        create_meeting.assert_not_called()

    def test_admin_online_interview_emails_zoom_join_url(self):
        candidate = SimpleNamespace(email="candidate@example.com", full_name="Taylor")
        job = SimpleNamespace(job_id=8, title="Analyst", location="Main Office")

        with self.app.app_context(), \
             patch.object(db.session, "get", side_effect=lambda model, key: candidate if model is Candidate else job), \
             patch.object(db.session, "add"), \
             patch.object(db.session, "commit"), \
             patch("app.services.interview_management_service.ZoomMeetingService.create_meeting", return_value="https://zoom.us/j/123") as create_meeting, \
             patch("app.services.interview_management_service.EmailService.send_interview_scheduled_email") as send_email:
            interview = InterviewManagementService.add(
                "3", "8", "2026-10-01", "09:30", "Online", "Recruiter", ""
            )

        self.assertEqual(interview.meeting_link, "https://zoom.us/j/123")
        create_meeting.assert_called_once_with(
            "Interview: Analyst", "2026-10-01", "09:30"
        )
        self.assertEqual(
            send_email.call_args.kwargs["meeting_link"], "https://zoom.us/j/123"
        )

    def test_recruiter_interview_uses_resume_match_and_emails_job_title(self):
        candidate = SimpleNamespace(email="candidate@example.com", full_name="Taylor")
        applied_job = SimpleNamespace(job_id=4, title="Support Agent", location="Old Office")
        matched_job = SimpleNamespace(job_id=9, title="Data Analyst", location="HQ")
        application = SimpleNamespace(
            candidate_id=3,
            candidate=candidate,
            job=applied_job,
        )

        with self.app.app_context(), \
             patch.object(db.session, "get", return_value=application), \
             patch.object(db.session, "add"), \
             patch.object(db.session, "commit"), \
             patch("app.services.recruiter_interview_service.JobMatchingService.get_best_matching_job", return_value={"job": matched_job, "score": 80}), \
             patch("app.services.recruiter_interview_service.EmailService.send_interview_scheduled_email") as send_email:
            interview = RecruiterInterviewService.create(
                14, "Recruiter", "2026-10-01", "09:30", "Offline"
            )

        self.assertEqual(interview.job_id, 9)
        self.assertEqual(interview.meeting_link, "HQ")
        self.assertEqual(send_email.call_args.kwargs["job_title"], "Data Analyst")
        self.assertEqual(send_email.call_args.kwargs["meeting_link"], "HQ")

    def test_candidate_interview_saves_resume_matched_job(self):
        candidate = SimpleNamespace(email="candidate@example.com", full_name="Taylor")
        job = SimpleNamespace(job_id=12, title="Backend Engineer", location="Office")

        with self.app.app_context(), \
             patch.object(db.session, "get", return_value=candidate), \
             patch.object(db.session, "add"), \
             patch.object(db.session, "commit"), \
             patch("app.services.interview_service.JobMatchingService.get_best_matching_job", return_value={"job": job, "score": 90}), \
             patch("app.services.interview_service.NotificationService.create"), \
             patch("app.services.interview_service.EmailService.send_interview_email") as send_email:
            interview = InterviewService.schedule(
                3, "Recruiter", "2026-10-01", "09:30", "Offline"
            )

        self.assertEqual(interview.job_id, 12)
        self.assertEqual(interview.meeting_link, "Office")
        self.assertEqual(send_email.call_args.args[7], "Backend Engineer")

    def test_zoom_meeting_uses_zoom_join_url(self):
        self.app.config.update(
            ZOOM_ACCOUNT_ID="account",
            ZOOM_CLIENT_ID="client",
            ZOOM_CLIENT_SECRET="secret",
            ZOOM_TIMEZONE="UTC",
            ZOOM_MEETING_DURATION_MINUTES=45,
        )
        token_response = Mock()
        token_response.json.return_value = {"access_token": "access-token"}
        meeting_response = Mock()
        meeting_response.json.return_value = {"join_url": "https://zoom.us/j/123"}

        with self.app.app_context(), patch(
            "app.services.zoom_meeting_service.requests.post",
            side_effect=[token_response, meeting_response],
        ) as post:
            link = ZoomMeetingService.create_meeting(
                "Interview: Analyst", "2026-10-01", "09:30"
            )

        self.assertEqual(link, "https://zoom.us/j/123")
        self.assertEqual(post.call_count, 2)
        self.assertEqual(
            post.call_args.kwargs["json"]["start_time"], "2026-10-01T09:30:00"
        )

    def test_zoom_meeting_requires_credentials(self):
        self.app.config["ZOOM_CLIENT_SECRET"] = ""

        with self.app.app_context(), self.assertRaises(ZoomMeetingError):
            ZoomMeetingService.create_meeting(
                "Interview", "2026-10-01", "09:30"
            )


if __name__ == "__main__":
    unittest.main()