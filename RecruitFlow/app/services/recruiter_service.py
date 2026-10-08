from werkzeug.security import generate_password_hash

from app.database.db import db
from app.models.user import User


class RecruiterService:

    @staticmethod
    def get_all_recruiters():

        return User.query.filter_by(
            role="Recruiter"
        ).all()

    @staticmethod
    def get_recruiter(user_id):

        return db.session.get(User, user_id)

    @staticmethod
    def add_recruiter(username, email, password):

        existing = User.query.filter_by(
            email=email
        ).first()

        if existing:
            return False

        recruiter = User(

            username=username,

            email=email,

            password=generate_password_hash(
                password
            ),

            role="Recruiter"

        )

        db.session.add(recruiter)

        db.session.commit()

        return True

    @staticmethod
    def update_recruiter(
        user_id,
        username,
        email,
        password
    ):

        recruiter = db.session.get(User, user_id)

        if recruiter is None:
            return False

        recruiter.username = username
        recruiter.email = email

        if password.strip():

            recruiter.password = generate_password_hash(
                password
            )

        db.session.commit()

        return True

    @staticmethod
    def delete_recruiter(user_id):

        recruiter = db.session.get(User, user_id)

        if recruiter is None:
            return False

        if recruiter.role != "Recruiter":
            return False

        db.session.delete(recruiter)

        db.session.commit()

        return True