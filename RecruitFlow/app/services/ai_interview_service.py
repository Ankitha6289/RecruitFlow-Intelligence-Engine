import json
import re
import uuid
from datetime import date, timedelta

from app.database.db import db
from app.models.ai_interview import AIInterview
from app.models.interview_questions import InterviewQuestion
from app.models.interview import Interview

try:
    from groq import Groq
except Exception:  # pragma: no cover - optional dependency fallback
    Groq = None

try:
    from google import genai
except Exception:
    genai = None

from config import Config


class AIInterviewService:

    @staticmethod
    def create(candidate_id, job_id, scheduled_date=None, scheduled_time=None):

        interview = AIInterview(

            candidate_id=candidate_id,

            job_id=job_id,

            interview_link=str(uuid.uuid4()),

            scheduled_date=scheduled_date,

            scheduled_time=scheduled_time,

            status="Pending"

        )

        db.session.add(interview)

        db.session.commit()

        return interview

    @staticmethod
    def build_ai_question_set(candidate, job):
        candidate_name = getattr(candidate, "full_name", "Candidate") or "Candidate"
        job_title = getattr(job, "title", "the role") or "the role"
        company = getattr(job, "company", "the company") or "the company"
        description = getattr(job, "description", "") or ""
        skills = getattr(job, "skills", "") or ""
        experience = getattr(job, "experience", "") or ""

        prompt = (
            f"You are creating an AI interview for {candidate_name} applying for {job_title} at {company}. "
            f"Job description: {description}. Skills: {skills}. Experience expectation: {experience}. "
            "Return a JSON object with keys hr_questions, technical_questions, coding_questions, "
            "scenario_questions, behavioral_questions, evaluation. Each key should contain an array of 3 concise questions."
        )

        if Config.GROQ_API_KEY and Groq is not None:
            try:
                client = Groq(api_key=Config.GROQ_API_KEY)
                completion = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    temperature=0.7,
                    messages=[
                        {
                            "role": "system",
                            "content": "You create structured interview questions in valid JSON."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    response_format={"type": "json_object"}
                )
                content = completion.choices[0].message.content
                payload = json.loads(content)
                return AIInterviewService._normalize_payload(payload)
            except Exception:
                pass

        technical_skill_context = f"{skills} {experience}".strip()

        return AIInterviewService._normalize_payload({
            "hr_questions": [
                f"Tell us about yourself and why you want this {job_title} opportunity at {company}.",
                f"How does your background prepare you for a role like {job_title}?",
                f"What motivates you to join {company}?"
            ],
            "technical_questions": [
                f"Describe how you would approach the key technical responsibilities of a {job_title} role.",
                f"What technical concepts are most relevant to {job_title} based on the job description and skills: {technical_skill_context}?",
                f"How would you explain your approach to solving a problem in this role using the required stack?"
            ],
            "coding_questions": [
                f"Show how you would structure a small solution for a {job_title} related problem.",
                f"What coding practices would you follow for this role?",
                f"How would you validate your implementation for this job?"
            ],
            "scenario_questions": [
                f"How would you handle a high-pressure scenario in a {job_title} project?",
                f"Describe how you would communicate progress to stakeholders in this role.",
                f"How would you prioritize tasks for a critical delivery in this role?"
            ],
            "behavioral_questions": [
                f"Tell us about a time you adapted quickly to a challenge relevant to {job_title}.",
                f"Describe a time you worked with a team to deliver results under pressure.",
                f"How do you handle feedback when working on a demanding project?"
            ],
            "evaluation": [
                f"Assess {candidate_name}'s fit for {job_title} and explain the strengths to highlight during the interview."
            ]
        })

    @staticmethod
    def _normalize_payload(payload):
        normalized = {}
        for key in [
            "hr_questions",
            "technical_questions",
            "coding_questions",
            "scenario_questions",
            "behavioral_questions",
            "evaluation"
        ]:
            value = payload.get(key, []) or []
            if isinstance(value, str):
                value = [value]
            elif not isinstance(value, list):
                value = [str(value)]
            normalized[key] = [str(item).strip() for item in value if str(item).strip()]

        for key in normalized:
            if not normalized[key]:
                normalized[key] = ["No questions generated yet."]

        return normalized

    @staticmethod
    def save_questions(candidate_id, job_id, questions):
        existing = InterviewQuestion.query.filter_by(candidate_id=candidate_id, job_id=job_id).first()

        if existing is None:
            existing = InterviewQuestion(
                candidate_id=candidate_id,
                job_id=job_id,
                hr_questions="\n".join(questions.get("hr_questions", [])),
                technical_questions="\n".join(questions.get("technical_questions", [])),
                coding_questions="\n".join(questions.get("coding_questions", [])),
                scenario_questions="\n".join(questions.get("scenario_questions", [])),
                behavioral_questions="\n".join(questions.get("behavioral_questions", [])),
                evaluation="\n".join(questions.get("evaluation", []))
            )
            db.session.add(existing)
        else:
            existing.hr_questions = "\n".join(questions.get("hr_questions", []))
            existing.technical_questions = "\n".join(questions.get("technical_questions", []))
            existing.coding_questions = "\n".join(questions.get("coding_questions", []))
            existing.scenario_questions = "\n".join(questions.get("scenario_questions", []))
            existing.behavioral_questions = "\n".join(questions.get("behavioral_questions", []))
            existing.evaluation = "\n".join(questions.get("evaluation", []))

        db.session.commit()
        return existing

    @staticmethod
    def generate_for_interview(candidate, job):
        questions = AIInterviewService.build_ai_question_set(candidate, job)
        if candidate is not None and job is not None:
            AIInterviewService.save_questions(candidate.candidate_id, job.job_id, questions)
        return questions

    @staticmethod
    def build_interview_report_payload(candidate, job, questions, transcript="", recommendation="Maybe", emotion="neutral", eye_contact="unknown", timer_seconds=0):
        transcript_text = (transcript or "").strip()
        question_count = sum(len(v) for v in questions.values() if isinstance(v, list)) if questions else 0
        confidence_matches = re.findall(r"\b(confident|strong|good|excellent|clear)\b", transcript_text.lower())
        score = min(100, 60 + len(confidence_matches) * 8 + (25 if recommendation == "Hire" else 10 if recommendation == "Maybe" else 0))

        summary = (
            f"{getattr(candidate, 'full_name', 'Candidate') or 'Candidate'} completed an AI interview for "
            f"{getattr(job, 'title', 'the role') or 'the role'} with {question_count} question prompts."
        )
        if transcript_text:
            summary += f" Transcript highlights: {transcript_text[:180]}"

        return {
            "candidate_name": getattr(candidate, "full_name", "Candidate") or "Candidate",
            "job_title": getattr(job, "title", "the role") or "the role",
            "questions": questions,
            "transcript": transcript_text,
            "recommendation": recommendation,
            "emotion": emotion,
            "eye_contact": eye_contact,
            "timer_seconds": timer_seconds,
            "score": score,
            "summary": summary,
        }

    @staticmethod
    def get_all():

        return AIInterview.query.all()

    @staticmethod
    def get(interview_id):

        return db.session.get(AIInterview, interview_id)

    @staticmethod
    def evaluate_answer(candidate, job, question, transcript):
        transcript_text = (transcript or "").strip()
        candidate_skills = ", ".join(
            skill.skill_name
            for skill in getattr(candidate, "skills", []) or []
            if getattr(skill, "skill_name", None)
        )
        job_skills = getattr(job, "skills", "") or ""
        job_description = getattr(job, "description", "") or ""
        prompt = (
            f"Evaluate this candidate's interview response for the {getattr(job, 'title', 'role')} role.\n"
            f"Required skills: {job_skills}\n"
            f"Job description: {job_description}\n"
            f"Parsed resume skills: {candidate_skills}\n"
            f"Question: {question}\n"
            f"Candidate answer: {transcript_text}\n"
            "Assess relevance, correctness, specificity, and evidence of the required skills. "
            "Do not assess protected characteristics or appearance. Return only a JSON object with "
            "score (0-100) and summary."
        )
        if Config.GEMINI_API_KEY and genai is not None:
            try:
                client = genai.Client(api_key=Config.GEMINI_API_KEY)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                output_text = getattr(response, "text", "") or ""
                if output_text:
                    try:
                        result = json.loads(
                            output_text.removeprefix("```json")
                            .removesuffix("```")
                            .strip()
                        )
                        score = max(0, min(100, float(result.get("score", 0))))
                        result["score"] = score
                        result["recommendation"] = "Selected" if score >= 70 else "Rejected"
                        return result
                    except Exception:
                        pass
            except Exception:
                pass

        if Config.GROQ_API_KEY and Groq is not None:
            try:
                client = Groq(api_key=Config.GROQ_API_KEY)
                completion = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    temperature=0.2,
                    messages=[
                        {
                            "role": "system",
                            "content": "Evaluate interview answers fairly using job-related evidence only. Return valid JSON.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    response_format={"type": "json_object"},
                )
                result = json.loads(completion.choices[0].message.content)
                score = max(0, min(100, float(result.get("score", 0))))
                result["score"] = score
                result["recommendation"] = "Selected" if score >= 70 else "Rejected"
                return result
            except Exception:
                pass

        positive = len(re.findall(r"\b(good|confident|strong|experienced|skilled|success|clear)\b", transcript_text.lower()))
        negative = len(re.findall(r"\b(unsure|maybe|not sure|difficult|problematic|weak|unclear)\b", transcript_text.lower()))
        base = 50 + positive * 8 - negative * 8
        score = max(0, min(100, base))
        recommendation = "Selected" if score >= 70 else "Rejected"
        summary = (
            f"Evaluation generated locally from transcript keywords. Score {score}, "
            f"recommendation {recommendation}."
        )
        return {
            "score": score,
            "recommendation": recommendation,
            "summary": summary
        }

    @staticmethod
    def finalize_candidate_interview(interview, transcript, duration_seconds, recording_path):
        from app.models.candidate import Candidate
        from app.models.offer import Offer
        from app.services.email_service import EmailService
        from app.services.offer_email_service import OfferEmailService

        if interview.status in {"Selected", "Rejected"}:
            return {
                "status": interview.status,
                "score": interview.ai_final_score,
            }

        candidate = db.session.get(Candidate, interview.candidate_id)
        if candidate is None or interview.job is None:
            return None

        saved_questions = InterviewQuestion.query.filter_by(
            candidate_id=interview.candidate_id,
            job_id=interview.job_id,
        ).first()
        question_text = "\n".join(
            getattr(saved_questions, field, "") or ""
            for field in (
                "hr_questions",
                "technical_questions",
                "coding_questions",
                "scenario_questions",
                "behavioral_questions",
            )
        )
        evaluation = AIInterviewService.evaluate_answer(
            candidate,
            interview.job,
            question_text or f"Interview for {interview.job.title}",
            transcript,
        )
        score = max(0, min(100, float(evaluation.get("score", 0))))
        status = "Selected" if score >= 70 else "Rejected"

        interview.status = status
        interview.ai_final_score = score
        interview.ai_transcript = transcript
        interview.ai_recording_path = recording_path
        interview.ai_duration_seconds = duration_seconds
        candidate.status = status
        db.session.commit()

        if candidate.email:
            if status == "Selected":
                today = date.today()
                offer = Offer(
                    candidate_id=candidate.candidate_id,
                    job_id=interview.job_id,
                    offer_date=today,
                    joining_date=today + timedelta(days=30),
                    salary=interview.job.salary or "To be discussed",
                    status="Pending",
                )
                db.session.add(offer)
                db.session.commit()
                try:
                    OfferEmailService.send_offer(candidate, offer)
                    print(f"[AIInterviewService] Offer email sent to {candidate.email}")
                except Exception as e:
                    print(f"[AIInterviewService] Offer email FAILED for {candidate.email}: {e}")
            else:
                try:
                    EmailService.rejection_email(candidate)
                    print(f"[AIInterviewService] Rejection email sent to {candidate.email}")
                except Exception as e:
                    print(f"[AIInterviewService] Rejection email FAILED for {candidate.email}: {e}")

        return {"status": status, "score": score}

    @staticmethod
    def get_by_link(link):

        return AIInterview.query.filter_by(

            interview_link=link

        ).first()

    @staticmethod
    def update_candidate_status_based_on_interview(interview_id, score, recommendation):
        """Automatically update candidate status based on AI interview result and send notification email."""
        from app.models.candidate import Candidate
        from app.services.email_service import EmailService

        interview = db.session.get(AIInterview, interview_id)
        if not interview:
            return False

        candidate = db.session.get(Candidate, interview.candidate_id)
        if not candidate:
            return False

        # Determine final status
        if recommendation == "Hire" and score >= 70:
            candidate.status = "Selected"
        elif recommendation == "Reject" or score < 40:
            candidate.status = "Rejected"
        else:
            candidate.status = "Under Review"

        # Mark interview completed
        interview.status = "Completed"
        db.session.commit()

        # Send result email
        if candidate.status == "Selected":
            EmailService.selection_email(candidate)
        elif candidate.status == "Rejected":
            EmailService.rejection_email(candidate)

        return True