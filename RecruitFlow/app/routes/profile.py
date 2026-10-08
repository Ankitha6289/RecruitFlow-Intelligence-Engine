from flask import Blueprint, render_template

from app.services.profile_service import ProfileService

profile_bp = Blueprint(
    "profile",
    __name__
)


@profile_bp.route("/candidate/<int:candidate_id>")
def profile(candidate_id):

    data = ProfileService.get_candidate_profile(candidate_id)

    print("========== DEBUG ==========")
    print(data)
    print("===========================")

    return render_template(
        "profile.html",
        data=data
    )