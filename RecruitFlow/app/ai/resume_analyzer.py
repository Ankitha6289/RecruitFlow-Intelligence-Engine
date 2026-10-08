import json

from app.ai.groq_client import client


class ResumeAnalyzer:

    @staticmethod
    def analyze(parsed_data):

        prompt = f"""
You are an AI Resume Analyzer.

Analyze this resume.

Resume Data:

{json.dumps(parsed_data, indent=2)}

Return ONLY valid JSON.

{{
    "candidate_summary":"",
    "technical_strengths":[],
    "weaknesses":[],
    "recommended_roles":[],
    "suitability_score":0
}}
"""

        response = client.chat.completions.create(

            model="qwen/qwen3.8-27b",

            messages=[
                {
                    "role": "system",
                    "content": "You are an expert HR Resume Analyzer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        result = response.choices[0].message.content.strip()

        if result.startswith("```"):
            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

        return json.loads(result)