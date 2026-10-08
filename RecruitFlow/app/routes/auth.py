from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.database.db import db
from app.models.user import User
from app.models.candidate import Candidate
from app.utils.auth_helpers import (
    find_candidate_by_email,
    normalize_email,
    upgrade_password_if_needed,
    verify_password,
)

from app.services.dashboard_service import DashboardService
from app.services.recruiter_dashboard_service import RecruiterDashboardService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService

auth_bp = Blueprint("auth", __name__)


# =====================================================
# REGISTER
# =====================================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        email = normalize_email(request.form["email"])
        password = request.form["password"]
        role = request.form["role"]

        existing_email = User.query.filter(
            db.func.lower(db.func.trim(User.email)) == email
        ).first()

        if existing_email:
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter(
            db.func.lower(db.func.trim(User.username)) == username.lower()
        ).first()

        if existing_user:
            flash("Username is already taken. Please choose another username.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role=role
        )

        db.session.add(user)
        db.session.commit()

        ActivityLogService.create(
            user.user_id,
            "New User Registered",
            "Authentication"
        )

        NotificationService.create(
            title="New User",
            message=f"{username} registered successfully.",
            notification_type="Authentication",
            recipient_role="Admin"
        )

        flash("Registration Successful.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# =====================================================
# LOGIN
# =====================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = normalize_email(request.form["email"])
        password = request.form["password"]

        user = User.query.filter(
            db.func.lower(db.func.trim(User.email)) == email
        ).first()

        if user:

            if check_password_hash(user.password, password):

                session.clear()

                session["user_id"] = user.user_id
                session["username"] = user.username
                session["role"] = user.role
                session["email"] = user.email

                ActivityLogService.create(
                    user.user_id,
                    "Logged into the system",
                    "Authentication"
                )

                NotificationService.create(
                    title="User Login",
                    message=f"{user.username} logged in.",
                    notification_type="Authentication",
                    recipient_role="Admin"
                )

                flash("Login Successful", "success")

                if user.role == "Admin":
                    return redirect(url_for("auth.admin_dashboard"))

                return redirect(url_for("auth.recruiter_dashboard"))

        candidate = find_candidate_by_email(email)

        if candidate:

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

                ActivityLogService.create(
                    None,
                    "Candidate Logged In",
                    "Authentication"
                )

                NotificationService.create(
                    title="Candidate Login",
                    message=f"{candidate.full_name} logged in.",
                    notification_type="Authentication",
                    recipient_role="Recruiter"
                )

                flash("Candidate Login Successful", "success")

                return redirect(
                    url_for("candidate_dashboard.dashboard")
                )

        flash("Invalid Email or Password", "danger")

    return render_template("login.html")


# =====================================================
# LOGOUT
# =====================================================

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully", "success")

    return redirect(url_for("auth.login"))


# =====================================================
# ADMIN DASHBOARD
# =====================================================

@auth_bp.route("/admin")
def admin_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Admin":
        flash("Access Denied", "danger")
        return redirect(url_for("auth.login"))

    data = DashboardService.get_dashboard_data()

    return render_template(
        "admin_dashboard.html",
        data=data,
        stats=data,
        **data
    )


# =====================================================
# RECRUITER DASHBOARD
# =====================================================

@auth_bp.route("/recruiter")
def recruiter_dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "Recruiter":
        flash("Access Denied", "danger")
        return redirect(url_for("auth.login"))

    data = RecruiterDashboardService.get_dashboard()

    return render_template(
        "recruiter_dashboard.html",
        data=data
    )