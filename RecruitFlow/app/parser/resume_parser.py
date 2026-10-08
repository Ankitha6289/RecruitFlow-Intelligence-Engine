import re

from app.utils.regex_patterns import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    LINKEDIN_PATTERN,
    GITHUB_PATTERN,
    PORTFOLIO_PATTERN,
    CGPA_PATTERN
)


class ResumeParser:

    SKILL_SET = [
        "Python", "Java", "C", "C++", "C#", "SQL",
        "MySQL", "Flask", "Django", "FastAPI",
        "HTML", "CSS", "JavaScript",
        "Bootstrap", "React", "Angular",
        "Node.js", "Express",
        "Git", "GitHub",
        "Docker", "Kubernetes",
        "Pandas", "NumPy",
        "TensorFlow", "PyTorch",
        "Machine Learning", "Deep Learning",
        "Power BI", "Excel", "Tableau",
        "AWS", "Azure", "GCP",
        "MongoDB", "PostgreSQL",
        "Redis", "Linux", "Spring Boot",
        "Hibernate", "Node", "ReactJS"
    ]

    LANGUAGES = [
        "English", "Hindi", "Kannada",
        "Tamil", "Telugu", "Malayalam"
    ]

    # Degree prefixes — must appear at the START of the line
    # or as standalone tokens to avoid matching mid-sentence
    EDUCATION_DEGREE_PATTERNS = [
        r"\bB\.?E\.?\b", r"\bB\.?Tech\.?\b", r"\bBTech\b",
        r"\bM\.?Tech\.?\b", r"\bMTech\b",
        r"\bMCA\b", r"\bBCA\b",
        r"\bMBA\b", r"\bBBA\b",
        r"\bB\.?Sc\.?\b", r"\bM\.?Sc\.?\b",
        r"\bPh\.?D\.?\b", r"\bDiploma\b",
        r"\bB\.?C\.?A\.?\b", r"\bM\.?C\.?A\.?\b",
        r"\bBachelor\b", r"\bMaster\b",
        r"\bPost\s*Graduate\b", r"\bUnder\s*Graduate\b",
    ]

    # Junk lines — never the candidate's name
    _NAME_IGNORE = {
        "resume", "curriculum vitae", "cv", "profile", "objective",
        "summary", "education", "experience", "projects", "skills",
        "technical skills", "certifications", "languages", "contact",
        "declaration", "personal details", "personal information",
        "references", "achievements", "hobbies", "interests",
        "about me", "career objective", "professional summary",
        "key skills", "core competencies",
    }

    # Junk WORDS that appear at the top of PDFs (watermarks, headers)
    _NAME_JUNK_WORDS = {
        "confidential", "private", "draft", "page", "updated",
        "version", "cisco", "microsoft", "google", "amazon",
        "apple", "accenture", "infosys", "wipro", "tcs",
    }

    # City / location words — a name line should not contain these
    _LOCATION_WORDS = {
        "bangalore", "bengaluru", "mumbai", "delhi", "hyderabad",
        "chennai", "pune", "kolkata", "ahmedabad", "jaipur",
        "karnataka", "maharashtra", "india", "usa", "uk",
        "street", "road", "avenue", "nagar", "layout", "colony",
        "district", "state", "city", "village", "town", "pin",
    }

    def __init__(self, text):
        self.text = text
        self.lines = [l.strip() for l in text.splitlines() if l.strip()]

    # ──────────────────────────────────────────────────────────
    # NAME
    # ──────────────────────────────────────────────────────────
    def extract_name(self):
        """
        Strategy:
        1. Find the email in the text.
        2. Look at lines BEFORE the email (the header block).
        3. From those lines pick the one that looks most like a name.
        Fallback: scan the first 25 lines with strict heuristics.
        """
        email = self.extract_email()

        # Determine which lines appear before the email
        header_lines = []
        for i, line in enumerate(self.lines):
            if email and email.lower() in line.lower():
                header_lines = self.lines[:i]
                break
        if not header_lines:
            header_lines = self.lines[:25]

        for line in reversed(header_lines):   # closest line above email first
            candidate = self._score_name_line(line)
            if candidate:
                return candidate

        # Fallback: full first-25 scan
        for line in self.lines[:25]:
            candidate = self._score_name_line(line)
            if candidate:
                return candidate

        return "Unknown Candidate"

    def _score_name_line(self, line):
        """Return cleaned name if line looks like a person's name, else None."""
        clean = line.strip()
        if not clean:
            return None

        lower = clean.lower()

        # Hard rejects
        if lower in self._NAME_IGNORE:
            return None
        if "@" in clean or "http" in lower or "www" in lower:
            return None
        if re.search(r"\d{5,}", clean):          # long number = phone/zip
            return None
        if ":" in clean or "|" in clean:          # label lines  "Phone: ..."
            return None
        if len(clean) > 60:                       # too long
            return None

        # Reject if any junk/company/location word is present
        words_lower = set(lower.split())
        if words_lower & self._NAME_JUNK_WORDS:
            return None
        if words_lower & self._LOCATION_WORDS:
            return None

        # Strip non-name characters
        cleaned = re.sub(r"[^A-Za-z .'`-]", "", clean).strip()
        words = cleaned.split()

        if len(words) < 2 or len(words) > 5:
            return None

        # Every significant word must be alphabetic
        for w in words:
            core = w.replace(".", "").replace("-", "").replace("'", "")
            if len(core) <= 1:
                continue
            if not core.isalpha():
                return None

        return cleaned.title()

    # ──────────────────────────────────────────────────────────
    # EMAIL
    # ──────────────────────────────────────────────────────────
    def extract_email(self):
        m = re.search(EMAIL_PATTERN, self.text, re.IGNORECASE)
        return m.group(0) if m else ""

    # ──────────────────────────────────────────────────────────
    # PHONE
    # ──────────────────────────────────────────────────────────
    def extract_phone(self):
        m = re.search(PHONE_PATTERN, self.text)
        return m.group(0) if m else ""

    # ──────────────────────────────────────────────────────────
    # LINKEDIN
    # ──────────────────────────────────────────────────────────
    def extract_linkedin(self):
        m = re.search(LINKEDIN_PATTERN, self.text, re.IGNORECASE)
        return m.group(0) if m else ""

    # ──────────────────────────────────────────────────────────
    # GITHUB
    # ──────────────────────────────────────────────────────────
    def extract_github(self):
        m = re.search(GITHUB_PATTERN, self.text, re.IGNORECASE)
        return m.group(0) if m else ""

    # ──────────────────────────────────────────────────────────
    # PORTFOLIO
    # ──────────────────────────────────────────────────────────
    def extract_portfolio(self):
        urls = re.findall(PORTFOLIO_PATTERN, self.text)
        for url in urls:
            low = url.lower()
            if "github" in low or "linkedin" in low:
                continue
            return url
        return ""

    # ──────────────────────────────────────────────────────────
    # SKILLS
    # ──────────────────────────────────────────────────────────
    def extract_skills(self):
        skills, text_lower = [], self.text.lower()
        for skill in self.SKILL_SET:
            if skill.lower() in text_lower:
                skills.append(skill)
        return sorted(set(skills))

    # ──────────────────────────────────────────────────────────
    # EDUCATION  (strict — degree keyword must be at line start
    #             or be a standalone token, not mid-sentence)
    # ──────────────────────────────────────────────────────────
    def extract_education(self):
        education = []
        degree_re = re.compile(
            "|".join(self.EDUCATION_DEGREE_PATTERNS),
            re.IGNORECASE
        )

        # Also accept lines that contain college/university if
        # they're short enough (< 120 chars) and look structural
        college_re = re.compile(
            r"\b(college|university|institute|school of)\b",
            re.IGNORECASE
        )

        for line in self.lines:
            # Must not be a long paragraph
            if len(line) > 150:
                continue

            # Degree keyword present
            if degree_re.search(line):
                # Exclude lines that are clearly sentences
                word_count = len(line.split())
                if word_count <= 20:
                    education.append(line)
                continue

            if college_re.search(line) and len(line.split()) <= 15:
                education.append(line)

        return list(dict.fromkeys(education))

    # ──────────────────────────────────────────────────────────
    # COLLEGE
    # ──────────────────────────────────────────────────────────
    def extract_college(self):
        for line in self.lines:
            lower = line.lower()
            if any(k in lower for k in ("college", "university", "institute", "school")):
                if len(line.split()) <= 15:
                    return line
        return ""

    # ──────────────────────────────────────────────────────────
    # CERTIFICATIONS
    # ──────────────────────────────────────────────────────────
    def extract_certifications(self):
        certs = []
        for line in self.lines:
            low = line.lower()
            if any(k in low for k in ("certificate", "certification", "certified")):
                certs.append(line)
        return list(dict.fromkeys(certs))

    # ──────────────────────────────────────────────────────────
    # PROJECTS
    # ──────────────────────────────────────────────────────────
    def extract_projects(self):
        projects, capture = [], False
        stop = {"education", "experience", "skills", "technical skills",
                "languages", "certifications", "declaration"}
        for line in self.lines:
            lower = line.lower()
            if re.match(r"^projects?\b", lower):
                capture = True
                continue
            if capture:
                if lower.strip() in stop:
                    capture = False
                    continue
                if len(line) > 5:
                    projects.append(line)
        return list(dict.fromkeys(projects))

    # ──────────────────────────────────────────────────────────
    # EXPERIENCE  (only meaningful experience lines)
    # ──────────────────────────────────────────────────────────
    def extract_experience(self):
        experience = []
        # Section-based capture
        section_re = re.compile(
            r"^(work\s+experience|professional\s+experience|experience|employment)\s*$",
            re.IGNORECASE
        )
        stop_re = re.compile(
            r"^(education|skills|projects|certifications|languages|"
            r"declaration|references|achievements|hobbies)\s*$",
            re.IGNORECASE
        )
        capture = False
        for line in self.lines:
            if section_re.match(line.strip()):
                capture = True
                continue
            if stop_re.match(line.strip()):
                capture = False
                continue
            if capture and len(line) > 5:
                experience.append(line)

        # If section capture found nothing, fall back to keyword scan
        if not experience:
            kw = re.compile(
                r"\b(intern|internship|developer|engineer|analyst|"
                r"trainee|worked at|worked in|joined)\b",
                re.IGNORECASE
            )
            for line in self.lines:
                if kw.search(line) and len(line.split()) <= 25:
                    experience.append(line)

        return list(dict.fromkeys(experience))

    # ──────────────────────────────────────────────────────────
    # INTERNSHIPS
    # ──────────────────────────────────────────────────────────
    def extract_internships(self):
        return list(dict.fromkeys(
            l for l in self.lines if "intern" in l.lower()
        ))

    # ──────────────────────────────────────────────────────────
    # LANGUAGES
    # ──────────────────────────────────────────────────────────
    def extract_languages(self):
        text_lower = self.text.lower()
        return list(dict.fromkeys(
            lang for lang in self.LANGUAGES if lang.lower() in text_lower
        ))

    # ──────────────────────────────────────────────────────────
    # CGPA
    # ──────────────────────────────────────────────────────────
    def extract_cgpa(self):
        m = re.search(CGPA_PATTERN, self.text)
        if m:
            return m.group(1)
        # Also try percentage
        m2 = re.search(r"([0-9]{2,3}(?:\.[0-9]+)?)\s*%", self.text)
        return m2.group(1) if m2 else ""

    # ──────────────────────────────────────────────────────────
    # YEARS OF EXPERIENCE
    # ──────────────────────────────────────────────────────────
    def extract_years_of_experience(self):
        m = re.search(r"(\d+)\+?\s*(?:years?|yrs?)", self.text, re.IGNORECASE)
        return m.group(1) if m else "0"

    # ──────────────────────────────────────────────────────────
    # MISSING FIELDS
    # ──────────────────────────────────────────────────────────
    def missing_fields(self):
        missing = []
        if self.extract_name() == "Unknown Candidate":
            missing.append("Name")
        if not self.extract_email():
            missing.append("Email")
        if not self.extract_phone():
            missing.append("Phone")
        if not self.extract_education():
            missing.append("Education")
        if not self.extract_skills():
            missing.append("Skills")
        return missing

    # ──────────────────────────────────────────────────────────
    # FINAL PARSE
    # ──────────────────────────────────────────────────────────
    def parse(self):
        return {
            "full_name":           self.extract_name(),
            "email":               self.extract_email(),
            "phone":               self.extract_phone(),
            "linkedin":            self.extract_linkedin(),
            "github":              self.extract_github(),
            "portfolio":           self.extract_portfolio(),
            "address":             "",
            "education":           self.extract_education(),
            "college":             self.extract_college(),
            "skills":              self.extract_skills(),
            "experience":          self.extract_experience(),
            "projects":            self.extract_projects(),
            "certifications":      self.extract_certifications(),
            "internships":         self.extract_internships(),
            "languages":           self.extract_languages(),
            "cgpa":                self.extract_cgpa(),
            "years_of_experience": self.extract_years_of_experience(),
            "missing_fields":      self.missing_fields(),
        }
