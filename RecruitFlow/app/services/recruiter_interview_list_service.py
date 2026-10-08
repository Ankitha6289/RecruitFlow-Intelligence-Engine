from app.database.db import db
from app.models.interview import Interview
from sqlalchemy.orm import joinedload


class RecruiterInterviewListService:

    @staticmethod
    def get_all():

        interviews = Interview.query.options(joinedload(Interview.proctor_events)).all()
        return RecruiterInterviewListService.annotate_proctor_risk(interviews)

    @staticmethod
    def get_by_id(interview_id):

        interview = Interview.query.options(joinedload(Interview.proctor_events)).get(interview_id)
        if interview:
            RecruiterInterviewListService.annotate_proctor_risk([interview])
        return interview

    @staticmethod
    def calculate_proctor_score(interview):

        weights = {
            "tab_switch": 15,
            "copy_attempt": 5,
            "paste_attempt": 5,
            "cut_attempt": 5,
            "right_click": 5,
            "focus_loss": 10,
            "window_resize": 10,
            "camera_away": 20
        }
        score = 0
        for event in getattr(interview, "proctor_events", []) or []:
            score += weights.get(event.event_type, 10)
        return score

    @staticmethod
    def get_risk_level(score):

        if score >= 51:
            return "High Risk"
        if score >= 21:
            return "Suspicious"
        return "Safe"

    @staticmethod
    def annotate_proctor_risk(interviews):

        for interview in interviews:
            score = RecruiterInterviewListService.calculate_proctor_score(interview)
            interview.proctor_score = score
            interview.proctor_risk = RecruiterInterviewListService.get_risk_level(score)
        return interviews


    @staticmethod
    def complete(interview_id):

        interview = db.session.get(Interview, interview_id)

        if interview:

            interview.status = "Completed"

            db.session.commit()


    @staticmethod
    def select(interview_id):

        interview = db.session.get(Interview, interview_id)

        if interview:

            interview.status = "Selected"

            db.session.commit()


    @staticmethod
    def reject(interview_id):

        interview = db.session.get(Interview, interview_id)

        if interview:

            interview.status = "Rejected"

            db.session.commit()


    @staticmethod
    def delete(interview_id):

        interview = db.session.get(Interview, interview_id)

        if interview:

            db.session.delete(interview)

            db.session.commit()