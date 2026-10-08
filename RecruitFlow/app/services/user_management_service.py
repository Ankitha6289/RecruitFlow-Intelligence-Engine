from app.database.db import db
from app.models.user import User


class UserManagementService:

    # -----------------------------------
    # Get All Users
    # -----------------------------------

    @staticmethod
    def get_all():

        return User.query.order_by(
            User.user_id.desc()
        ).all()

    # -----------------------------------
    # Search User
    # -----------------------------------

    @staticmethod
    def search(keyword):

        return User.query.filter(

            User.username.ilike(f"%{keyword}%")

        ).all()

    # -----------------------------------
    # Get User
    # -----------------------------------

    @staticmethod
    def get(user_id):

        return db.session.get(User, user_id)

    # -----------------------------------
    # Update User
    # -----------------------------------

    @staticmethod
    def update(

        user_id,

        username,

        email,

        role

    ):

        user = db.session.get(User, user_id)

        if not user:
            return None

        user.username = username
        user.email = email
        user.role = role

        db.session.commit()

        return user

    # -----------------------------------
    # Delete User
    # -----------------------------------

    @staticmethod
    def delete(user_id):

        user = db.session.get(User, user_id)

        if user:

            db.session.delete(user)

            db.session.commit()

    # -----------------------------------
    # Activate / Deactivate User
    # -----------------------------------

    @staticmethod
    def toggle_status(user_id):

        user = db.session.get(User, user_id)

        if user:

            user.is_active = not user.is_active

            db.session.commit()

            return user

        return None