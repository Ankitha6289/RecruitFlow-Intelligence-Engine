from app.services.ai_interview_service import AIInterviewService


class DummyCandidate:
    def __init__(self):
        self.full_name = "Jane Doe"
        self.email = "jane@example.com"


class DummyJob:
    def __init__(self):
        self.title = "Python Developer"
        self.company = "RecruitFlow"
        self.description = "Build REST APIs using Flask and SQL"
        self.skills = "Python, Flask, SQL"


def test_build_ai_question_set_uses_job_context():
    candidate = DummyCandidate()
    job = DummyJob()

    payload = AIInterviewService.build_ai_question_set(candidate, job)

    assert payload["hr_questions"]
    assert any("Python Developer" in question for question in payload["hr_questions"])
    assert payload["technical_questions"]
    assert any("Flask" in question for question in payload["technical_questions"])


def test_build_interview_report_payload_includes_recommendation_and_metrics():
    candidate = DummyCandidate()
    job = DummyJob()
    questions = AIInterviewService.build_ai_question_set(candidate, job)

    payload = AIInterviewService.build_interview_report_payload(
        candidate=candidate,
        job=job,
        questions=questions,
        transcript="I am confident about building APIs.",
        recommendation="Hire",
        emotion="calm",
        eye_contact="good",
        timer_seconds=75,
    )

    assert payload["recommendation"] == "Hire"
    assert payload["score"] >= 0
    assert payload["summary"]
