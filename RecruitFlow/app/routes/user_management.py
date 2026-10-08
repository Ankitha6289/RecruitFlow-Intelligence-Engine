from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app.services.user_management_service import UserManagementService
from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService

user_management_bp = Blueprint(
    "user_management",
    __name__
)


# =====================================================
# View Users
# =====================================================

@user_management_bp.route("/admin/users")
def users():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    keyword = request.args.get("keyword", "").strip()

    if keyword:
        users = UserManagementService.search(keyword)
    else:
        users = UserManagementService.get_all()

    return render_template(

        "users.html",

        users=users,

        keyword=keyword

    )


# =====================================================
# Edit User
# =====================================================

@user_management_bp.route(
    "/admin/users/edit/<int:user_id>",
    methods=["GET", "POST"]
)
def edit_user(user_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = UserManagementService.get(user_id)

    if user is None:

        flash(
            "User not found.",
            "danger"
        )

        return redirect(
            url_for("user_management.users")
        )

    if request.method == "POST":

        UserManagementService.update(

            user_id,

            request.form["username"],

            request.form["email"],

            request.form["role"]

        )

        ActivityLogService.create(

            session["user_id"],

            "Updated User",

            "User Management"

        )

        NotificationService.create(

            title="User Updated",

            message="User information updated successfully.",

            notification_type="User",

            recipient_role="Admin"

        )

        flash(

            "User updated successfully.",

            "success"

        )

        return redirect(
            url_for("user_management.users")
        )

    return render_template(

        "edit_user.html",

        user=user

    )


# =====================================================
# Activate / Deactivate User
# =====================================================

@user_management_bp.route("/admin/users/toggle/<int:user_id>")
def toggle_user(user_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = UserManagementService.toggle_status(user_id)

    if user:

        ActivityLogService.create(

            session["user_id"],

            "Changed User Status",

            "User Management"

        )

        NotificationService.create(

            title="User Status Changed",

            message=f"{user.username} account status updated.",

            notification_type="User",

            recipient_role="Admin"

        )

        flash(
            "User status updated.",
            "success"
        )

    return redirect(
        url_for("user_management.users")
    )


# =====================================================
# Delete User
# =====================================================

@user_management_bp.route("/admin/users/delete/<int:user_id>")
def delete_user(user_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    UserManagementService.delete(user_id)

    ActivityLogService.create(

        session["user_id"],

        "Deleted User",

        "User Management"

    )

    NotificationService.create(

        title="User Deleted",

        message="A user account has been deleted.",

        notification_type="User",

        recipient_role="Admin"

    )

    flash(
        "User deleted successfully.",
        "success"
    )

    return redirect(
        url_for("user_management.users")
    )