# ResumeIQ 🚀

An AI-powered resume analyzer built with Django. Upload your resume and get instant feedback — keyword analysis, ATS score, skill gap detection, and AI-generated suggestions powered by Google Gemini and Groq.

---

## Features

- **AI Resume Analysis** — Gemini 2.5 Flash analyzes your resume with Groq as fallback
- **ATS Score** — See how well your resume passes Applicant Tracking Systems
- **Keyword Analysis** — Detects missing keywords for your target job role
- **Skill Gap Detection** — Identifies what skills to learn next
- **User Authentication** — Email login + Google OAuth via django-allauth
- **Password Reset** — Email-based reset via Gmail SMTP
- **Responsive UI** — Works on desktop and mobile

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2 |
| Database | PostgreSQL (Neon cloud / local Docker) |
| AI | Google Gemini 2.5 Flash + Groq (llama-3.3-70b) |
| Auth | django-allauth (email + Google OAuth) |
| Static Files | WhiteNoise |
| PDF Parsing | PyMuPDF + pdf2image + Tesseract OCR |
| Deployment | Render |
| Containerization | Docker + Docker Compose |

---

## Docker Support 🐳

This project is fully Dockerized for local development.

### What's inside `docker-compose.yml`

```yaml
services:
  db:   # PostgreSQL 17 container (commented out — using Neon cloud DB by default)
  web:  # Django app container built from the local Dockerfile
```

### Run with Docker

```bash
# 1. Copy the env template and fill in your values
cp .env.example .env

# 2. Build and start containers
docker-compose up --build

# 3. App runs at http://localhost:8000
```

### Dockerfile

```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

## Database Setup

The app uses a priority-based database config in `settings.py`:

1. **If `DATABASE_URL` is set** → connects to Neon (cloud PostgreSQL)
2. **If `DATABASE_URL` is not set** → connects to local PostgreSQL via individual `DB_*` env vars (perfect for Docker)

---

## Local Setup (without Docker)

```bash
# Clone the repo
git clone https://github.com/k4rtikx/ResumeIQ.git
cd ResumeIQ

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your real values

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DATABASE_URL` | Neon PostgreSQL connection string |
| `DB_NAME / DB_USER / DB_PASSWORD` | Local PostgreSQL credentials |
| `GEMINI_API_KEY` | Google Gemini API key |
| `GROQ_API_KEY` | Groq API key (free fallback LLM) |
| `EMAIL_HOST_USER` | Gmail address for sending emails |
| `EMAIL_HOST_PASSWORD` | Gmail App Password |
| `RAZORPAY_KEY_ID / KEY_SECRET` | Razorpay payment keys |

> ⚠️ **Never commit your `.env` file.** It is gitignored.

---

## Security

- `.env` is in `.gitignore` — API keys and passwords are never pushed to GitHub
- `SECRET_KEY` is loaded from environment variable
- `DEBUG=False` in production
- WhiteNoise handles static files securely

---

## Deployment

Deployed on **Render** using Gunicorn with a custom `gunicorn.conf.py` (timeout set to 120s to handle Gemini API response times).

---

## Learning Log

This project was built as a learning exercise covering:
- Django (models, views, templates, auth)
- PostgreSQL integration
- Google Gemini & Groq AI APIs
- Docker & Docker Compose
- Deployment on Render
- JWT tokens *(coming soon)*
