from werkzeug.security import generate_password_hash, check_password_hash

from app.database.db import db
from app.models.user import User


class RecruiterProfileService:

    @staticmethod
    def get_user(user_id):
        return db.session.get(User, user_id)

    @staticmethod
    def update_profile(user_id, username, email):

        user = db.session.get(User, user_id)

        if user:

            user.username = username
            user.email = email

            db.session.commit()

        return user

    @staticmethod
    def change_password(user_id, current_password, new_password):

        user = db.session.get(User, user_id)

        if not user:
            return False, "User not found."

        if not check_password_hash(user.password, current_password):
            return False, "Current password is incorrect."

        user.password = generate_password_hash(new_password)

        db.session.commit()

        return True, "Password changed successfully."