from app.database.db import db
from app.models.candidate import Candidate
from app.models.skills import Skill
from app.models.ats_analysis import ATSAnalysis


class ATSService:

    REQUIRED_KEYWORDS = [
        "python",
        "sql",
        "flask",
        "html",
        "css",
        "javascript",
        "mysql",
        "git",
        "api",
        "communication"
    ]

    @staticmethod
    def build_ats_result(candidate_skills):
        normalized_skills = {
            skill.lower().strip()
            for skill in candidate_skills
            if skill
        }

        matched = []
        missing = []

        for keyword in ATSService.REQUIRED_KEYWORDS:
            if keyword in normalized_skills:
                matched.append(keyword)
            else:
                missing.append(keyword)

        ats_score = int((len(matched) / len(ATSService.REQUIRED_KEYWORDS)) * 100)

        if len(missing) > 0:
            suggestions = (
                "Matched skills: "
                + ", ".join(matched)
                + ". Improve your resume by adding these skills: "
                + ", ".join(missing)
            )
        else:
            suggestions = (
                "Matched skills: "
                + ", ".join(matched)
                + ". Excellent ATS Resume."
            )

        return {
            "matched": matched,
            "missing": missing,
            "ats_score": ats_score,
            "suggestions": suggestions,
        }

    @staticmethod
    def analyze(candidate_id):

        candidate = db.session.get(Candidate, candidate_id)

        if not candidate:
            return None

        skills = Skill.query.filter_by(candidate_id=candidate_id).all()

        candidate_skills = [
            skill.skill_name.lower()
            for skill in skills
        ]

        ats_result = ATSService.build_ats_result(candidate_skills)

        existing = ATSAnalysis.query.filter_by(
            candidate_id=candidate_id
        ).first()

        if existing:

            existing.ats_score = ats_result["ats_score"]
            existing.matched_keywords = ", ".join(ats_result["matched"])
            existing.missing_keywords = ", ".join(ats_result["missing"])
            existing.suggestions = ats_result["suggestions"]

        else:

            report = ATSAnalysis(
                candidate_id=candidate_id,
                ats_score=ats_result["ats_score"],
                matched_keywords=", ".join(ats_result["matched"]),
                missing_keywords=", ".join(ats_result["missing"]),
                suggestions=ats_result["suggestions"]
            )

            db.session.add(report)

        db.session.commit()

        return ATSAnalysis.query.filter_by(
            candidate_id=candidate_id
        ).first()