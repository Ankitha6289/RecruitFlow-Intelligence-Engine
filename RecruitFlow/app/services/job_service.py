from app.database.db import db
from app.models.job import Job
from app.services.notification_service import NotificationService

class JobService:

    @staticmethod
    def get_all():
        return Job.query.all()

    @staticmethod
    def get(job_id):
        return db.session.get(Job, job_id)

    @staticmethod
    def add(data):

        job = Job(

            title=data["title"],

            company=data["company"],

            location=data["location"],

            experience=data["experience"],

            salary=data["salary"],

            skills=data["skills"],

            description=data["description"]

        )

        db.session.add(job)
        db.session.commit()
        NotificationService.create(
    title="New Job Posted",
    message=f"{job.title} has been posted.",
    notification_type="Job",
    recipient_role="Candidate"
)

    @staticmethod
    def update(job_id, data):

        job = db.session.get(Job, job_id)

        job.title = data["title"]
        job.company = data["company"]
        job.location = data["location"]
        job.experience = data["experience"]
        job.salary = data["salary"]
        job.skills = data["skills"]
        job.description = data["description"]

        db.session.commit()


    @staticmethod
    def delete(job_id):

        job = db.session.get(Job, job_id)

        db.session.delete(job)

        db.session.commit()
    @staticmethod
    def search(keyword):

      return Job.query.filter(

        (Job.title.ilike(f"%{keyword}%")) |

        (Job.company.ilike(f"%{keyword}%")) |

        (Job.location.ilike(f"%{keyword}%"))

    ).all()