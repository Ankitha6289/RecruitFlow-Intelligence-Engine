# Requirements Document

## Introduction

This document captures the requirements for the **Resume Parsing + AI Analysis** feature of the RecruitFlow Flask application. The feature extends the existing upload pipeline to provide reliable multi-format resume ingestion, structured data extraction, Gemini-powered candidate intelligence, and role recommendation scoring — all persisted to the MySQL database for downstream recruiter workflows.

The system builds on the existing `app/parser/`, `app/ai/`, and `app/services/` infrastructure, filling gaps identified in the current implementation (Gemini integration stub, single-score role recommendation, missing fields such as achievements and soft skills, and lack of batch-upload error isolation).

---

## Glossary

- **Upload_Service**: The Flask route and associated service responsible for receiving resume files from HTTP requests and orchestrating the parsing pipeline.
- **File_Validator**: The component responsible for checking that uploaded files conform to supported formats and size limits before processing.
- **Resume_Extractor**: The component (`app/parser/extractor.py`) that reads raw bytes from PDF or DOCX files and returns plain text.
- **Resume_Parser**: The component (`app/parser/resume_parser.py`) that applies regex and keyword matching to extracted text to produce a structured dictionary of candidate fields.
- **Candidate_Service**: The service (`app/services/candidate_service.py`) that persists parsed candidate data (core profile, education, experience, skills) to the MySQL database.
- **AI_Engine**: The Gemini-backed module (`app/ai_engine/gemini.py`) that receives structured parsed data and returns AI-generated candidate intelligence.
- **AI_Analysis_Service**: The service (`app/services/ai_analysis_service.py`) that calls AI_Engine, maps the response to the `AIAnalysis` model, and commits results to the database.
- **Role_Recommender**: The logic within AI_Analysis_Service responsible for producing per-role suitability percentages.
- **Candidate**: A SQLAlchemy model (`candidates` table) representing a job applicant extracted from a resume.
- **AIAnalysis**: A SQLAlchemy model (`ai_analysis` table) storing AI-generated summary, recommended roles, suitability scores, strengths, and weaknesses for a Candidate.
- **Parsed_Data**: The Python dictionary returned by Resume_Parser containing all extracted candidate fields.
- **Suitability_Score**: A numeric percentage (0–100) indicating how well a candidate fits a specific job role.
- **Recruiter**: A user with recruiter or HR role who uploads resumes and reviews analysis results.

---

## Requirements

### Requirement 1: Multi-File Resume Upload

**User Story:** As a Recruiter, I want to upload multiple resumes at once, so that I can process an entire candidate batch without repeated manual uploads.

#### Acceptance Criteria

1. WHEN a Recruiter submits a file upload request containing one or more files, THE Upload_Service SHALL accept all files in a single HTTP POST request.
2. THE File_Validator SHALL accept only files with `.pdf` or `.docx` extensions.
3. IF a submitted file has an extension other than `.pdf` or `.docx`, THEN THE File_Validator SHALL reject that file and record a per-file failure message without halting processing of the remaining files.
4. IF a submitted file exceeds 10 MB, THEN THE File_Validator SHALL reject that file and record a per-file failure message without halting processing of the remaining files.
5. WHEN the upload request completes, THE Upload_Service SHALL return a summary indicating the count of successfully processed files and the count of failed files with their individual error reasons.
6. IF no valid files are present in the upload request, THEN THE Upload_Service SHALL return an error response indicating that no processable files were received.

---

### Requirement 2: Resume Text Extraction

**User Story:** As a Recruiter, I want the system to extract readable text from uploaded resumes, so that downstream parsing can operate on clean text regardless of the file format.

#### Acceptance Criteria

1. WHEN a `.pdf` file is provided, THE Resume_Extractor SHALL extract all text content from every page using the PyMuPDF (`fitz`) library.
2. WHEN a `.docx` file is provided, THE Resume_Extractor SHALL extract all paragraph text from the document using the `python-docx` library.
3. IF text extraction produces an empty string, THEN THE Resume_Extractor SHALL raise a `ValueError` with a message indicating the file yielded no extractable text.
4. THE Resume_Extractor SHALL return extracted text as a UTF-8 string.

---

### Requirement 3: Structured Data Extraction (Parsing)

**User Story:** As a Recruiter, I want the system to identify and extract specific fields from resume text, so that candidate data is stored in a structured, queryable format.

#### Acceptance Criteria

1. WHEN resume text is provided, THE Resume_Parser SHALL extract the candidate's full name, email address, and phone number.
2. WHEN resume text is provided, THE Resume_Parser SHALL extract LinkedIn URL, GitHub URL, and portfolio URL where present.
3. WHEN resume text is provided, THE Resume_Parser SHALL extract the list of technical skills by matching against the predefined skill vocabulary.
4. WHEN resume text is provided, THE Resume_Parser SHALL extract education entries (degree keywords), college/institution name, and CGPA or percentage where present.
5. WHEN resume text is provided, THE Resume_Parser SHALL extract work experience entries, internship entries, and project descriptions.
6. WHEN resume text is provided, THE Resume_Parser SHALL extract certifications, languages known, and total years of experience.
7. WHEN resume text is provided, THE Resume_Parser SHALL extract achievements, soft skills, and technical skill categories.
8. WHEN a required field (name, email, phone, education, skills, experience) cannot be extracted, THE Resume_Parser SHALL include that field name in a `missing_fields` list within Parsed_Data.
9. THE Resume_Parser SHALL return all extracted fields as a single Parsed_Data dictionary.

---

### Requirement 4: Candidate and Related Data Persistence

**User Story:** As a Recruiter, I want parsed candidate data saved to the database, so that candidate profiles are available for search, ranking, and downstream workflows.

#### Acceptance Criteria

1. WHEN Parsed_Data is received, THE Candidate_Service SHALL create a new `Candidate` record if no existing candidate with the same email address exists.
2. WHEN Parsed_Data is received and a `Candidate` record with the same email already exists, THE Candidate_Service SHALL update the existing record's fields with the new values rather than creating a duplicate.
3. THE Candidate_Service SHALL persist each education entry as a separate `Education` record linked to the Candidate.
4. THE Candidate_Service SHALL persist each experience entry as a separate `Experience` record linked to the Candidate.
5. THE Candidate_Service SHALL persist each skill as a separate `Skill` record linked to the Candidate, with `skill_type` set to `"Technical"` for skills from the predefined vocabulary.
6. IF any database operation raises an exception during persistence, THEN THE Candidate_Service SHALL roll back the entire transaction and re-raise the exception so the Upload_Service can record the failure.
7. THE Candidate_Service SHALL store the uploaded file's filename in the `resume_path` field of the `Candidate` record.

---

### Requirement 5: AI-Powered Candidate Intelligence

**User Story:** As a Recruiter, I want the system to generate an AI summary and identify a candidate's strengths, weaknesses, and domain expertise, so that I can quickly assess candidate suitability without reading the full resume.

#### Acceptance Criteria

1. WHEN Parsed_Data is available for a candidate, THE AI_Engine SHALL send a structured prompt containing all parsed fields to the Gemini API.
2. THE AI_Engine SHALL return a response containing: `candidate_summary`, `technical_strengths`, `weaknesses`, `seniority_level`, `domain_expertise`, and `strongest_skills`.
3. IF the Gemini API call fails or returns a non-parseable response, THEN THE AI_Analysis_Service SHALL fall back to a deterministic summary built from the parsed skills and experience fields, without raising an unhandled exception.
4. THE AI_Engine SHALL parse the Gemini API response as JSON, stripping markdown code fences if present before parsing.
5. WHEN an AI response is obtained, THE AI_Analysis_Service SHALL persist the result as an `AIAnalysis` record linked to the Candidate.
6. THE AI_Analysis_Service SHALL update an existing `AIAnalysis` record if one already exists for the Candidate, rather than creating a duplicate.

---

### Requirement 6: Role Recommendation with Suitability Scores

**User Story:** As a Recruiter, I want to see a ranked list of suitable job roles with percentage scores for each candidate, so that I can match candidates to open positions efficiently.

#### Acceptance Criteria

1. WHEN AI analysis completes, THE Role_Recommender SHALL produce a list of at least three recommended job roles for the candidate.
2. EACH recommended role SHALL have an associated Suitability_Score expressed as a percentage between 0 and 100.
3. THE Role_Recommender SHALL order recommended roles in descending order of Suitability_Score.
4. THE AI_Analysis_Service SHALL persist recommended roles and their Suitability_Scores as a structured JSON string in the `recommended_roles` and `suitability_scores` fields of the `AIAnalysis` record.
5. IF the AI_Engine returns fewer than three roles, THEN THE Role_Recommender SHALL supplement the list with fallback roles derived from the candidate's extracted skills to reach a minimum of three recommendations.

---

### Requirement 7: End-to-End Pipeline Orchestration

**User Story:** As a Recruiter, I want the upload, parse, save, and analyse steps to execute automatically when a resume is uploaded, so that I do not need to trigger each step manually.

#### Acceptance Criteria

1. WHEN a resume file passes validation, THE Upload_Service SHALL invoke the full pipeline: text extraction → parsing → candidate persistence → AI analysis — in that order.
2. IF any pipeline step raises an exception for a given file, THEN THE Upload_Service SHALL record the failure for that file, roll back any partial database writes for that file, and continue processing the remaining files in the batch.
3. WHEN the full pipeline completes successfully for a file, THE Candidate_Service SHALL create an `ActivityLog` entry and a `Notification` record indicating successful resume processing.
4. THE Upload_Service SHALL NOT expose raw exception stack traces in the HTTP response returned to the Recruiter.

---

### Requirement 8: Gemini AI Integration

**User Story:** As a system administrator, I want the AI analysis to use the Gemini API so that the platform uses the intended AI provider for candidate intelligence.

#### Acceptance Criteria

1. THE AI_Engine SHALL authenticate with the Gemini API using an API key read from the application configuration (environment variable `GEMINI_API_KEY`).
2. THE AI_Engine SHALL use the `google-generativeai` Python SDK to send prompts to the Gemini model.
3. THE AI_Engine SHALL use a prompt that instructs the model to return only valid JSON matching the expected response schema.
4. IF `GEMINI_API_KEY` is absent or empty at startup, THEN THE AI_Engine SHALL log a warning and allow the system to fall back to the deterministic analysis path defined in Requirement 5.3.
5. THE AI_Engine SHALL set a request timeout such that Gemini API calls that exceed 30 seconds are cancelled and the fallback path is invoked.
