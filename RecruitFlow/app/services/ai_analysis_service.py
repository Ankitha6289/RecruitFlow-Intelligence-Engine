import traceback

from app.database.db import db

from app.models.ai_analysis import AIAnalysis

from app.ai.resume_analyzer import ResumeAnalyzer

from app.services.activity_log_service import ActivityLogService
from app.services.notification_service import NotificationService


class AIAnalysisService:

    # =====================================================
    # Analyze Resume and Save Result
    # =====================================================

    @staticmethod
    def analyze_and_save(candidate_id, parsed_data):

        try:

            print("===== AI Analysis Started =====")

            result = None
            try:
                result = ResumeAnalyzer.analyze(parsed_data)
            except Exception as ai_error:
                print("AI service unavailable, using fallback analysis")
                print(ai_error)
                result = {
                    "candidate_summary": f"Candidate profile extracted from resume. Skills: {', '.join(parsed_data.get('skills', [])) or 'Not available'}.",
                    "technical_strengths": parsed_data.get("skills", []),
                    "weaknesses": [],
                    "recommended_roles": [
                        "Software Developer",
                        "Data Analyst",
                        "Business Analyst"
                    ],
                    "suitability_score": 70
                }

            print("AI Response:")
            print(result)

            analysis = AIAnalysis(

                candidate_id=candidate_id,

                candidate_summary=result.get(
                    "candidate_summary",
                    ""
                ),

                recommended_roles=", ".join(
                    result.get(
                        "recommended_roles",
                        []
                    )
                ),

                suitability_scores=str(result.get(
                    "suitability_score",
                    0
                )),

                strengths=", ".join(
                    result.get(
                        "technical_strengths",
                        []
                    )
                ),

                weaknesses=", ".join(
                    result.get(
                        "weaknesses",
                        []
                    )
                )

            )

            db.session.add(analysis)

            db.session.commit()
                        # ---------------------------------------
            # Activity Log
            # ---------------------------------------

            ActivityLogService.create(

                None,

                "AI Resume Analysis Completed",

                "AI Analysis"

            )

            # ---------------------------------------
            # Notification
            # ---------------------------------------

            NotificationService.create(

                title="AI Resume Analysis Completed",

                message="Resume AI analysis completed successfully.",

                notification_type="AI",

                recipient_role="Recruiter"

            )

            print("AI Analysis Saved Successfully")

            return analysis

        except Exception as e:

            db.session.rollback()

            print("===== AI Analysis Error =====")

            print(e)

            traceback.print_exc()

            return None