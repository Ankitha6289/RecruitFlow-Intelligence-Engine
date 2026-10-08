import os
import tempfile
import unittest
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import patch

from app import create_app
from app.database.db import db
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.models.interview_questions import InterviewQuestion
from app.services.ai_interview_service import AIInterviewService
from config import Config


class AIInterviewCompletionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True

    def _interview(self):
        return SimpleNamespace(
            interview_id=41,
            candidate_id=7,
            job_id=9,
            job=SimpleNamespace(
                title="Backend Engineer",
                salary="$100,000",
            ),
            status="Scheduled",
            ai_final_score=None,
            ai_transcript=None,
            ai_recording_path=None,
            ai_duration_seconds=None,
        )

    def test_selected_candidate_gets_offer_email_and_session_is_saved(self):
        interview = self._interview()
        candidate = SimpleNamespace(
            candidate_id=7,
            email="candidate@example.com",
            status="Applied",
        )
        questions = SimpleNamespace(
            hr_questions="Tell me about yourself.",
            technical_questions="Explain APIs.",
            coding_questions="",
            scenario_questions="",
            behavioral_questions="",
        )

        with self.app.app_context(), \
             patch.object(db.session, "get", return_value=candidate), \
             patch.object(db.session, "add") as add, \
             patch.object(db.session, "commit"), \
             patch.object(InterviewQuestion, "query") as question_query, \
             patch.object(AIInterviewService, "evaluate_answer", return_value={"score": 82}), \
             patch("app.services.offer_email_service.OfferEmailService.send_offer") as send_offer:
            question_query.filter_by.return_value.first.return_value = questions
            result = AIInterviewService.finalize_candidate_interview(
                interview, "Candidate answer transcript", 175, "ai_interviews/session.webm"
            )

        self.assertEqual(result, {"status": "Selected", "score": 82.0})
        self.assertEqual(interview.status, "Selected")
        self.assertEqual(candidate.status, "Selected")
        self.assertEqual(interview.ai_transcript, "Candidate answer transcript")
        self.assertEqual(interview.ai_recording_path, "ai_interviews/session.webm")
        self.assertEqual(interview.ai_duration_seconds, 175)
        offer = add.call_args.args[0]
        self.assertEqual(offer.job_id, interview.job_id)
        self.assertEqual(offer.salary, "$100,000")
        send_offer.assert_called_once_with(candidate, offer)

    def test_rejected_candidate_receives_rejection_email_only(self):
        interview = self._interview()
        candidate = SimpleNamespace(candidate_id=7, email="candidate@example.com", status="Applied")

        with self.app.app_context(), \
             patch.object(db.session, "get", return_value=candidate), \
             patch.object(db.session, "add") as add, \
             patch.object(db.session, "commit"), \
             patch.object(InterviewQuestion, "query") as question_query, \
             patch.object(AIInterviewService, "evaluate_answer", return_value={"score": 42}), \
             patch("app.services.email_service.EmailService.rejection_email") as rejection_email, \
             patch("app.services.offer_email_service.OfferEmailService.send_offer") as send_offer:
            question_query.filter_by.return_value.first.return_value = None
            result = AIInterviewService.finalize_candidate_interview(
                interview, "Candidate answer transcript", 90, "ai_interviews/session.webm"
            )

        self.assertEqual(result["status"], "Rejected")
        self.assertEqual(interview.status, "Rejected")
        self.assertEqual(candidate.status, "Rejected")
        rejection_email.assert_called_once_with(candidate)
        send_offer.assert_not_called()
        add.assert_not_called()

    def test_candidate_completion_uploads_recording_and_transcript(self):
        interview = self._interview()
        upload_dir = tempfile.TemporaryDirectory()
        self.addCleanup(upload_dir.cleanup)
        self.app.config["UPLOAD_FOLDER"] = upload_dir.name
        client = self.app.test_client()
        with client.session_transaction() as session:
            session["candidate_id"] = interview.candidate_id

        with patch("app.routes.candidate_interviews.db.session.get", return_value=interview), \
             patch("app.routes.candidate_interviews.AIInterviewService.finalize_candidate_interview", return_value={"status": "Selected", "score": 84}) as finalize:
            response = client.post(
                "/candidate/interview-complete",
                data={
                    "interview_id": str(interview.interview_id),
                    "transcript": "Full session transcript",
                    "duration_seconds": "123",
                    "recording": (BytesIO(b"webm data"), "session.webm"),
                },
                content_type="multipart/form-data",
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "Selected")
        saved_path = finalize.call_args.args[3]
        self.assertTrue(os.path.isfile(os.path.join(upload_dir.name, saved_path)))
        self.assertEqual(finalize.call_args.args[1], "Full session transcript")
        self.assertEqual(finalize.call_args.args[2], 123)

    def test_staff_recording_requires_staff_session_and_streams_video(self):
        interview = self._interview()
        interview.ai_recording_path = "ai_interviews/session.webm"
        upload_dir = tempfile.TemporaryDirectory()
        self.addCleanup(upload_dir.cleanup)
        self.app.config["UPLOAD_FOLDER"] = upload_dir.name
        recording_dir = os.path.join(upload_dir.name, "ai_interviews")
        os.makedirs(recording_dir)
        with open(os.path.join(recording_dir, "session.webm"), "wb") as recording_file:
            recording_file.write(b"webm data")

        client = self.app.test_client()
        self.assertEqual(client.get("/staff/interviews/41/ai-recording").status_code, 302)
        with client.session_transaction() as session:
            session["user_id"] = 1
        with patch("app.routes.candidate_interviews.db.session.get", return_value=interview):
            response = client.get("/staff/interviews/41/ai-recording")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "video/webm")
        self.assertEqual(response.data, b"webm data")
        response.close()

    def test_ai_evaluation_uses_job_and_resume_context_and_binary_decision(self):
        client = unittest.mock.Mock()
        client.models.generate_content.return_value.text = (
            '{"score": 76, "summary": "Evidence matches the role requirements."}'
        )
        candidate = SimpleNamespace(
            skills=[SimpleNamespace(skill_name="Python")]
        )
        job = SimpleNamespace(
            title="Backend Engineer",
            skills="Python, SQL",
            description="Build and maintain API services.",
        )

        with patch.object(Config, "GEMINI_API_KEY", "test-key"), \
             patch("app.services.ai_interview_service.genai.Client", return_value=client):
            result = AIInterviewService.evaluate_answer(
                candidate,
                job,
                "How would you design an API?",
                "I have built Python APIs backed by SQL databases.",
            )

        self.assertEqual(result["score"], 76)
        self.assertEqual(result["recommendation"], "Selected")
        evaluation_prompt = client.models.generate_content.call_args.kwargs["contents"]
        self.assertIn("Parsed resume skills: Python", evaluation_prompt)
        self.assertIn("Build and maintain API services", evaluation_prompt)


if __name__ == "__main__":
    unittest.main()