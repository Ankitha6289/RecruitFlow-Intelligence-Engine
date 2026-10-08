from app.models.user import User
from app.database.db import db


class AdminProfileService:

    @staticmethod
    def get_profile(user_id):

        return db.session.get(User, user_id)


    @staticmethod
    def update_profile(

        user_id,

        username,

        email

    ):

        user = db.session.get(User, user_id)

        if not user:
            return None

        user.username = username
        user.email = email

        db.session.commit()

        return user