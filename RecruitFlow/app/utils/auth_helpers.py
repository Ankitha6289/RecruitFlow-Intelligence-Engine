from werkzeug.security import check_password_hash, generate_password_hash

from app.database.db import db


def normalize_email(email):
    if not email:
        return ""
    return email.strip().lower()


def find_candidate_by_email(email):
    from app.models.candidate import Candidate

    normalized = normalize_email(email)
    if not normalized:
        return None

    return Candidate.query.filter(
        db.func.lower(db.func.trim(Candidate.email)) == normalized
    ).first()


def is_valid_password_hash(stored_password):
    if not stored_password:
        return False
    return stored_password.startswith("scrypt:") or stored_password.startswith("pbkdf2:")


def verify_password(stored_password, plain_password):
    if not stored_password or not plain_password:
        return False, False

    if is_valid_password_hash(stored_password):
        return check_password_hash(stored_password, plain_password), False

    # Legacy plain-text passwords from older records
    if stored_password == plain_password:
        return True, True

    return False, False


def upgrade_password_if_needed(candidate, plain_password, needs_upgrade):
    if needs_upgrade and plain_password:
        candidate.password = generate_password_hash(plain_password)
        db.session.commit()
