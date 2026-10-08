from flask import Blueprint
from flask import render_template
from flask import request

from app.models.candidate import Candidate
from app.services.search_service import SearchService
search_bp = Blueprint(
    "search",
    __name__
)


@search_bp.route("/search")
@search_bp.route("/search-candidates")
def search():

    keyword = request.args.get("keyword", "").strip()

    if keyword:

        candidates = SearchService.search_candidates(keyword)
        skills = SearchService.search_by_skill(keyword)

    else:

        # Show all candidates when no search keyword
        candidates = Candidate.query.all()
        skills = []

    return render_template(
        "search.html",
        candidates=candidates,
        skills=skills,
        keyword=keyword
    )
