from groq import Groq
from flask import current_app

from app.database.db import db
from app.models.candidate import Candidate
from app.models.skills import Skill
from app.models.education import Education
from app.models.experience import Experience
from app.models.chatbot_history import ChatbotHistory


class ChatbotService:

    @staticmethod
    def ask(candidate_id, question):

        candidate = db.session.get(Candidate, candidate_id)

        if not candidate:
            raise Exception("Candidate not found.")

        skills = Skill.query.filter_by(
            candidate_id=candidate_id
        ).all()

        education = Education.query.filter_by(
            candidate_id=candidate_id
        ).all()

        experience = Experience.query.filter_by(
            candidate_id=candidate_id
        ).all()

        skill_text = ", ".join(
            [s.skill_name for s in skills]
        )

        education_text = "\n".join(
            [e.degree for e in education]
        )

        experience_text = "\n".join(
            [f"{x.role} at {x.company_name}" for x in experience]
        )

        client = Groq(
            api_key=current_app.config["GROQ_API_KEY"]
        )

        prompt = f"""
You are an AI Resume Assistant.

Candidate Name:
{candidate.full_name}

Email:
{candidate.email}

Skills:
{skill_text}

Education:
{education_text}

Experience:
{experience_text}

Recruiter Question:

{question}

Answer only based on the candidate information.
If the information is unavailable, clearly say that it is not available.
"""

        response = client.chat.completions.create(

            model="qwen/qwen3.8-27b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.5,

            max_tokens=1000

        )

        answer = response.choices[0].message.content

        chat = ChatbotHistory(

            candidate_id=candidate_id,

            user_question=question,

            ai_answer=answer

        )

        db.session.add(chat)

        db.session.commit()

        return chat