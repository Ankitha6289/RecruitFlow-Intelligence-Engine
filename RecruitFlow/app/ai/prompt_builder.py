class PromptBuilder:

    @staticmethod
    def build(candidate):

        return f"""
You are an expert HR recruiter.

Analyze the following candidate.

Name:
{candidate['full_name']}

Education:
{candidate['education']}

Skills:
{candidate['skills']}

Experience:
{candidate['experience']}

Projects:
{candidate['projects']}

Internships:
{candidate['internships']}

Languages:
{candidate['languages']}

CGPA:
{candidate['cgpa']}

Return ONLY valid JSON.

Required keys:

candidate_summary

technical_strengths

weaknesses

suitability_score

recommended_roles
"""