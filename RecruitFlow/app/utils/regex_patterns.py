import re

EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

PHONE_PATTERN = r"(?:\+91[- ]?)?[6-9]\d{9}"

LINKEDIN_PATTERN = r"https?://(?:www\.)?linkedin\.com/[^\s]+"

GITHUB_PATTERN = r"https?://(?:www\.)?github\.com/[^\s]+"

PORTFOLIO_PATTERN = r"https?://[^\s]+"

CGPA_PATTERN = r"\b(?:CGPA|GPA)[:\s]*([0-9]+(?:\.[0-9]+)?)"

PERCENTAGE_PATTERN = r"([0-9]{2}(?:\.[0-9]+)?)\s*%"