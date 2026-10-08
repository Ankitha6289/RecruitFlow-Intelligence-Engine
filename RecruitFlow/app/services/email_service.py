from flask_mail import Message

from app.extensions import mail



class EmailService:

    @staticmethod
    def send_email(to, subject, body):
        try:
            msg = Message(
                subject=subject,
                recipients=[to]
            )
            msg.body = body
            mail.send(msg)
            print("=" * 50)
            print("EMAIL SENT SUCCESSFULLY")
            print("To      :", to)
            print("Subject :", subject)
            print("=" * 50)
        except Exception as e:
            print("=" * 50)
            print("EMAIL FAILED")
            print("To      :", to)
            print("Subject :", subject)
            print("Error   :", e)
            print("=" * 50)
            raise  # re-raise so callers can catch and surface the error

    @staticmethod
    def interview_email(candidate):

        subject = "Interview Invitation - RecruitFlow"


        body = f"""

Hello {candidate.full_name},


Congratulations!


You have been shortlisted for an interview.


Please login to RecruitFlow to check your interview schedule.


Regards,

RecruitFlow Team

"""


        EmailService.send_email(
            candidate.email,
            subject,
            body
        )


    @staticmethod
    def send_interview_email(candidate_email, candidate_name, interviewer, interview_date, interview_time, mode, meeting_link=None, job_title="the position"):
        """Legacy method — kept for backward compatibility."""
        EmailService.send_interview_scheduled_email(
            candidate_email=candidate_email,
            candidate_name=candidate_name,
            job_title=job_title,
            interviewer=interviewer,
            interview_date=interview_date,
            interview_time=interview_time,
            mode=mode,
            meeting_link=meeting_link
        )

    @staticmethod
    def send_interview_scheduled_email(
        candidate_email,
        candidate_name,
        job_title,
        interviewer,
        interview_date,
        interview_time,
        mode,
        meeting_link=None
    ):
        subject = "Interview Scheduled – RecruitFlow"

        if mode == "Online":
            location_line = f"Meeting Link : {meeting_link}"
            mode_note = "Please join the meeting using the link above at the scheduled time."
        else:
            location_line = f"Venue        : {meeting_link or 'Company Office'}"
            mode_note = "Please arrive at the venue 10 minutes before the scheduled time."

        body = f"""Hello {candidate_name},

Congratulations! You have been shortlisted for an interview for {job_title}.

────────────────────────────────
  INTERVIEW DETAILS
────────────────────────────────
  Interviewer  : {interviewer}
  Date         : {interview_date}
  Time         : {interview_time}
  Mode         : {mode}
  {location_line}
────────────────────────────────

{mode_note}

If you have any questions, please contact our HR team.

Best regards,
RecruitFlow Team
"""

        EmailService.send_email(candidate_email, subject, body)




    @staticmethod
    def selection_email(candidate):

        subject = "Congratulations - Selected"


        body = f"""

Dear {candidate.full_name},


Congratulations!


You have been selected for the position.


Our HR team will contact you soon.


Regards,

RecruitFlow Team

"""


        EmailService.send_email(
            candidate.email,
            subject,
            body
        )





    @staticmethod
    def rejection_email(candidate):


        subject = "Recruitment Update"


        body = f"""

Dear {candidate.full_name},


Thank you for applying.


Unfortunately, we cannot proceed with your application.


We wish you success in your career.


Regards,

RecruitFlow Team

"""


        EmailService.send_email(
            candidate.email,
            subject,
            body
        )





    @staticmethod
    def offer_email(candidate):
        subject = "Offer Letter - RecruitFlow"
        body = f"""
Dear {candidate.full_name},


Congratulations!


Your offer letter has been generated.


Please login to RecruitFlow.


Regards,

RecruitFlow Team

"""
        EmailService.send_email(
            candidate.email,
            subject,
            body
        )

    @staticmethod
    def send_status_email(candidate_email, candidate_name, status):
        """Send a status-update email when an interview record is edited.
        Called from InterviewService.update()."""

        if status == "Selected":
            subject = "Interview Result – You've Been Selected! – RecruitFlow"
            body = f"""Dear {candidate_name},

Congratulations! We are pleased to inform you that you have been SELECTED
following your recent interview.

Our HR team will be in touch shortly with the next steps.

Best regards,
RecruitFlow HR Team
"""
        elif status == "Rejected":
            subject = "Interview Outcome – RecruitFlow"
            body = f"""Dear {candidate_name},

Thank you for attending the interview with us.

After careful consideration, we regret to inform you that we are unable to
move forward with your application at this time.

We appreciate the time you invested and wish you every success in your
future endeavors.

Best regards,
RecruitFlow HR Team
"""
        else:
            subject = f"Interview Status Update – {status} – RecruitFlow"
            body = f"""Dear {candidate_name},

This is a notification that your interview status has been updated to: {status}.

Please log in to your RecruitFlow portal for more details.

Best regards,
RecruitFlow HR Team
"""

        try:
            EmailService.send_email(candidate_email, subject, body)
        except Exception as e:
            print(f"[EmailService] send_status_email failed for {candidate_email}: {e}")