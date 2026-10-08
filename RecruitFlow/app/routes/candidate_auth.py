from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import generate_password_hash

from app.database.db import db
from app.models.candidate import Candidate
from app.utils.auth_helpers import (
    find_candidate_by_email,
    is_valid_password_hash,
    normalize_email,
    upgrade_password_if_needed,
    verify_password,
)

candidate_auth_bp = Blueprint(
    "candidate_auth",
    __name__
)


# ----------------------------------
# Candidate Registration
# ----------------------------------
@candidate_auth_bp.route("/candidate/register", methods=["GET", "POST"])
def register():

    # Already logged in
    if "candidate_id" in session:
        return redirect(url_for("candidate_dashboard.dashboard"))

    if request.method == "POST":

        full_name = request.form["full_name"].strip()
        email = normalize_email(request.form["email"])
        phone = request.form["phone"].strip()
        password = request.form["password"]

        existing = find_candidate_by_email(email)

        if existing:
            flash("Email already registered.", "danger")
            return redirect(url_for("candidate_auth.register"))

        candidate = Candidate(
            full_name=full_name,
            email=email,
            phone=phone,
            password=generate_password_hash(password),
            status="Applied"
        )

        db.session.add(candidate)
        db.session.commit()

        flash("Registration Successful. Please Login.", "success")

        return redirect(url_for("candidate_auth.login"))

    return render_template("candidates/register.html")


# ----------------------------------
# Candidate Login
# ----------------------------------
@candidate_auth_bp.route("/candidate/login", methods=["GET", "POST"])
def login():

    # Already logged in
    if "candidate_id" in session:
        return redirect(url_for("candidate_dashboard.dashboard"))

    if request.method == "POST":

        email = normalize_email(request.form["email"])
        password = request.form["password"]

        candidate = find_candidate_by_email(email)

        if candidate:

            if not is_valid_password_hash(candidate.password):

                flash(
                    "Your account password was not set up correctly. "
                    "Use Forgot/Reset password or contact support.",
                    "danger"
                )

            else:

                password_ok, needs_upgrade = verify_password(
                    candidate.password,
                    password
                )

                if password_ok:

                    upgrade_password_if_needed(
                        candidate,
                        password,
                        needs_upgrade
                    )

                    session.clear()

                    session["candidate_id"] = candidate.candidate_id
                    session["candidate_name"] = candidate.full_name
                    session["candidate_email"] = candidate.email
                    session["role"] = "Candidate"

                    flash(
                        "Login Successful",
                        "success"
                    )

                    return redirect(
                        url_for("candidate_dashboard.dashboard")
                    )

                else:

                    flash(
                        "Wrong Password",
                        "danger"
                    )

        else:

            flash(
                "Candidate Email Not Found",
                "danger"
            )

    return render_template(
        "candidates/login.html"
    )

# ----------------------------------
# Candidate Logout
# ----------------------------------
@candidate_auth_bp.route("/candidate/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully", "success")

    return redirect(url_for("candidate_auth.login"))
@candidate_auth_bp.route("/reset_candidate_password")
def reset_candidate_password():

    email = normalize_email(
        request.args.get("email", "snehasa900@gmail.com")
    )
    new_password = request.args.get("password", "123456")

    candidate = find_candidate_by_email(email)

    if not candidate:
        return f"Candidate not found for email: {email}"

    candidate.password = generate_password_hash(new_password)

    db.session.commit()

    return (
        f"Password reset successfully for {candidate.email}. "
        f"Try logging in with password: {new_password}"
    )