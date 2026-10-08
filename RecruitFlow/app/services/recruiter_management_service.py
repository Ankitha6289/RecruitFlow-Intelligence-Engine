from werkzeug.security import generate_password_hash

from app.database.db import db
from app.models.user import User
from werkzeug.security import generate_password_hash

class RecruiterManagementService:

    # ----------------------------------------
    # Get All Recruiters
    # ----------------------------------------

    @staticmethod
    def get_all():

        return User.query.filter_by(

            role="Recruiter"

        ).order_by(

            User.user_id.desc()

        ).all()

    # ----------------------------------------
    # Search Recruiters
    # ----------------------------------------

    @staticmethod
    def search(keyword):

        return User.query.filter(

            User.role == "Recruiter",

            User.username.ilike(f"%{keyword}%")

        ).all()

    # ----------------------------------------
    # Get Recruiter
    # ----------------------------------------

    @staticmethod
    def get(user_id):

        return db.session.get(User, user_id)

    # ----------------------------------------
    # Add Recruiter
    # ----------------------------------------

    @staticmethod
    def add(

        username,

        email,

        password

    ):

        recruiter = User(

            username=username,

            email=email,

            password=generate_password_hash(password),

            role="Recruiter",

            is_active=True

        )

        db.session.add(recruiter)

        db.session.commit()

        return recruiter

    # ----------------------------------------
    # Update Recruiter
    # ----------------------------------------


@staticmethod
def update(user_id, username, email, password=None):

    recruiter = db.session.get(User, user_id)

    if recruiter:

        recruiter.username = username
        recruiter.email = email

        if password:

            recruiter.password = generate_password_hash(password)

        db.session.commit()

    return recruiter
    

    # ----------------------------------------
    # Activate / Deactivate
    # ----------------------------------------

    @staticmethod
    def toggle_status(user_id):

        recruiter = db.session.get(User, user_id)

        if recruiter:

            recruiter.is_active = not recruiter.is_active

            db.session.commit()

        return recruiter

    # ----------------------------------------
    # Delete Recruiter
    # ----------------------------------------

    @staticmethod
    def delete(user_id):

        recruiter = db.session.get(User, user_id)

        if recruiter:

            db.session.delete(recruiter)

            db.session.commit()