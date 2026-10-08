from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from app.database.db import db
from app.models.user import User
from app.models.candidate import Candidate


class ChangePasswordService:

    # ==========================================
    # Admin / Recruiter Password Change
    # ==========================================

    @staticmethod
    def change_user_password(

        user_id,

        old_password,

        new_password

    ):

        user = db.session.get(User, user_id)

        if not user:

            return False, "User not found."

        if not check_password_hash(

            user.password,

            old_password

        ):

            return False, "Old password is incorrect."

        user.password = generate_password_hash(
            new_password
        )

        db.session.commit()

        return True, "Password updated successfully."

    # ==========================================
    # Candidate Password Change
    # ==========================================

    @staticmethod
    def change_candidate_password(

        candidate_id,

        old_password,

        new_password

    ):

        candidate = db.session.get(Candidate, candidate_id)

        if not candidate:

            return False, "Candidate not found."

        if not check_password_hash(

            candidate.password,

            old_password

        ):

            return False, "Old password is incorrect."

        candidate.password = generate_password_hash(
            new_password
        )

        db.session.commit()

        return True, "Password updated successfully."