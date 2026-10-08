# ⚡ RecruitFlow — AI-Powered Recruitment Intelligence Platform

> A full-stack Flask web application that automates the entire hiring pipeline — from resume parsing and AI interviews to offer management, proctoring, and real-time analytics.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [User Roles](#user-roles)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [Running the App](#running-the-app)
- [Key Modules](#key-modules)
- [Screenshots](#screenshots)
- [API Integrations](#api-integrations)

---

## Overview

RecruitFlow is an end-to-end AI-powered recruitment management system built with Python/Flask. It supports three distinct user roles — **Admin**, **Recruiter**, and **Candidate** — each with their own portal, dashboard, and feature set.

The platform automates resume parsing, AI-driven interview sessions with real-time fraud detection, offer letter generation with PDF attachments, ATS scoring, skill gap analysis, and smart job matching.

---

## Features

### 🔐 Authentication
- Separate login/register flows for Admin/Recruiter and Candidate
- Session-based auth with role-based access control
- Password hashing with Werkzeug
- Change password with strength meter

### 👑 Admin Portal
- **Executive Command Center** dashboard with live KPI cards
- User, Recruiter, and Candidate management
- Job posting management (Add / Edit / Delete)
- Interview scheduling with Online (Google Meet / Zoom) and Offline modes
- Offer letter generation with auto PDF + email dispatch
- Scoring Dashboard with AI + ATS score rankings
- Analytics dashboard with Chart.js charts
- Reports with PDF/Excel export
- Skill Gap analysis
- AI Job Matching
- Notifications, Activity Logs, Backup & Restore
- System settings (company info, AI model, maintenance mode)

### 🧑‍💼 Recruiter Portal
- Recruiter dashboard with pipeline overview
- Candidate search with AI feature shortcuts
- Application management (shortlist / reject)
- Interview scheduling and proctor review
- Offer management
- Advanced analytics with Chart.js
- Job management

### 🎓 Candidate Portal
- Candidate dashboard with application status
- Resume upload (PDF/DOCX) with auto-parsing
- AI Resume Chatbot (ask questions about your resume)
- ATS Score report
- AI Mock Interview with proctoring
- Job browsing and one-click application
- Offer acceptance/decline
- Interview history and reports
- Profile and settings management

### 🤖 AI Features
- **Resume Parser** — extracts name, email, phone, skills, education, experience from PDF/DOCX
- **AI Interview** — browser-based interview with:
  - Speech-to-text question answering
  - MediaPipe FaceMesh face detection (up to 4 faces)
  - COCO-SSD object detection (phone, laptop, etc.)
  - Real-time fraud scoring (tab switches, DevTools, fullscreen exits, audio anomalies)
  - WebRTC video recording saved as `.webm`
- **AI Scoring** — Gemini 2.5 Flash + Groq fallback for answer evaluation (0–100 score)
- **ATS Analysis** — keyword matching between resume and job requirements
- **Skill Gap Analysis** — matched vs. missing skills with AI recommendations
- **Job Matching** — neural skill-based candidate-to-job matching with % score
- **Offer Letter PDF** — ReportLab-generated offer letters sent via email

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.x, Flask 3.1 |
| **Database** | MySQL + SQLAlchemy 2.0 + Flask-Migrate |
| **Authentication** | Flask session, Werkzeug password hashing |
| **AI / LLM** | Google Gemini 2.5 Flash, Groq (Qwen 3.8B-27B) |
| **Resume Parsing** | PyMuPDF, pdfplumber, python-docx, docx2txt |
| **Email** | Flask-Mail (Gmail SMTP / App Password) |
| **PDF Generation** | ReportLab |
| **Excel Export** | openpyxl, pandas |
| **Charts** | Chart.js 4.4.0 (CDN) |
| **Face Detection** | MediaPipe FaceMesh 0.4, TensorFlow.js 4.13 |
| **Object Detection** | COCO-SSD (TensorFlow.js) |
| **Video Recording** | MediaRecorder API (WebM) |
| **Speech** | Web Speech API (SpeechRecognition + SpeechSynthesis) |
| **Meetings** | Zoom Server-to-Server OAuth (with Google Meet fallback) |
| **Frontend** | Jinja2 templates, Bootstrap Icons, Inter font, custom CSS |
| **Server** | Gunicorn (production), Flask dev server (local) |

---

## Project Structure

```
RecruitFlow/
├── app/
│   ├── __init__.py              # App factory — registers all blueprints
│   ├── extensions.py            # Flask-Mail singleton
│   ├── ai/                      # Groq client, prompt builder, resume analyzer
│   ├── controllers/             # Admin management controllers (jobs, candidates, interviews, reports)
│   ├── database/                # db.py (SQLAlchemy instance)
│   ├── models/                  # All SQLAlchemy models
│   │   ├── user.py              # Admin / Recruiter users
│   │   ├── candidate.py         # Candidate accounts
│   │   ├── job.py               # Job postings
│   │   ├── interview.py         # Interviews + AI fields
│   │   ├── offer.py             # Offer letters
│   │   ├── ai_analysis.py       # AI suitability scores
│   │   ├── ats_analysis.py      # ATS keyword scores
│   │   ├── interview_proctor_event.py  # Fraud detection events
│   │   └── ...                  # 20+ models total
│   ├── parser/                  # PDF/DOCX resume parsers + extractor
│   ├── reports/                 # Offer generator (legacy disk-based)
│   ├── routes/                  # 49 Blueprint route files
│   ├── services/                # Business logic layer (40+ service classes)
│   ├── static/                  # CSS, JS, uploaded files
│   └── templates/               # Jinja2 HTML templates
│       ├── admin_base.html      # Admin portal base (dark ECC design)
│       ├── recruiter_base.html  # Recruiter portal base (dark violet)
│       ├── candidate_base.html  # Candidate portal base
│       ├── admin_dashboard.html # Executive Command Center
│       ├── candidates/          # Candidate-facing templates
│       ├── jobs/                # Job management templates
│       └── reports/             # Reports dashboard
├── config.py                    # Flask configuration (env-driven)
├── main.py                      # App entry point
├── requirements.txt             # Python dependencies
├── .env                         # Local secrets (never commit)
├── .env.example                 # Environment variable template
└── Procfile                     # Gunicorn production command
```

---

## User Roles

| Role | Login URL | Access |
|---|---|---|
| **Admin** | `/login` | Full platform access — all portals, settings, backup |
| **Recruiter** | `/login` | Candidate search, interviews, offers, analytics |
| **Candidate** | `/candidate/login` | Own profile, jobs, interviews, chatbot, offers |

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- Git

### 1. Clone the repository
```bash
git clone https://github.com/your-username/recruitflow.git
cd recruitflow/RecruitFlow
```

### 2. Create a virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Then edit `.env` with your actual values (see [Environment Variables](#environment-variables) below).

### 5. Update `config.py` database URI
Edit `config.py` and update the MySQL connection string:
```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost/recruitflow"
```

---

## Environment Variables

Create a `.env` file in the `RecruitFlow/` directory:

```env
# AI Keys
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key

# Gmail (SMTP) — use a 16-char App Password (no spaces)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=yourapppassword     # No spaces — strip them from the Google display format
MAIL_DEFAULT_SENDER=your_email@gmail.com

# Zoom Server-to-Server OAuth (optional — falls back to Google Meet)
ZOOM_ACCOUNT_ID=your_zoom_account_id
ZOOM_CLIENT_ID=your_zoom_client_id
ZOOM_CLIENT_SECRET=your_zoom_client_secret
ZOOM_TIMEZONE=UTC
ZOOM_MEETING_DURATION_MINUTES=60
```

### Getting a Gmail App Password
1. Enable **2-Step Verification** on your Google account at [myaccount.google.com/security](https://myaccount.google.com/security)
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Create a new App Password (App: Mail, Device: Other → "RecruitFlow")
4. Copy the 16-character password and paste it into `.env` **without spaces**

### Getting Groq API Key
- Sign up at [console.groq.com](https://console.groq.com) → API Keys → Create new key

### Getting Gemini API Key
- Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey) → Create API key

---

## Database Setup

### Create the MySQL database
```sql
CREATE DATABASE recruitflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Run migrations
```bash
flask db init        # First time only
flask db migrate -m "Initial migration"
flask db upgrade
```

### Create the first Admin user
After running the app, register at `/register` and select **Admin** as the role.

---

## Running the App

### Development
```bash
# From the RecruitFlow/ directory
python main.py
```
App runs at `http://127.0.0.1:5000`

### Production (Gunicorn)
```bash
gunicorn main:app
```

---

## Key Modules

### AI Interview + Fraud Detection
Located in `app/templates/candidates/ai_interview.html` and `app/services/ai_interview_service.py`.

**Fraud detection events tracked:**

| Event | Weight | Severity |
|---|---|---|
| DevTools opened | 35 | High |
| Phone/object detected | 30 | High |
| Multiple faces in frame | 25 | High |
| Camera away (>5s) | 20 | Medium |
| Fullscreen exit | 18 | Medium |
| Tab switch | 15 | Medium |
| Audio anomaly | 12 | Medium |
| Window resize | 10 | Low |
| Focus loss | 10 | Medium |
| Copy/paste attempt | 5 | Low |
| Eye contact loss | 5 | Low |

Risk levels: **Safe** (<21), **Suspicious** (21–50), **High Risk** (≥51)

### Email Flows
| Trigger | Email sent |
|---|---|
| Interview scheduled | Interview details + meeting link |
| Interview status updated | Selected / Rejected notification |
| AI interview — Selected | Offer letter with PDF attachment |
| AI interview — Rejected | Rejection email |
| Offer generated manually | Offer letter with PDF attachment |

### Resume Parsing
Supports PDF (PyMuPDF, pdfplumber) and DOCX (python-docx, docx2txt). Extracts:
- Full name, email, phone
- Skills (matched against a skills database)
- Education history
- Work experience

---

## API Integrations

| Service | Purpose | Fallback |
|---|---|---|
| **Google Gemini 2.5 Flash** | Interview answer scoring, AI analysis | Groq |
| **Groq (Qwen 3.8B-27B)** | Question generation, answer evaluation | Keyword scoring |
| **Zoom Server-to-Server OAuth** | Online meeting link generation | Google Meet placeholder |
| **Gmail SMTP** | All email notifications + offer PDFs | — |

---

## Security Notes

- All passwords hashed with Werkzeug `generate_password_hash`
- Session-based auth with `SECRET_KEY`
- Auth checks on every route — admin, recruiter, and candidate routes are separated
- `.env` file contains all secrets — **never commit it to version control**
- `.gitignore` should include `.env`, `uploads/`, `backups/`, `__pycache__/`, `.venv/`

---

## License

This project is developed for educational and demonstration purposes.

---

*Built with ❤️ using Flask, Python, and AI — RecruitFlow Intelligence Engine*
