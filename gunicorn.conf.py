# Gunicorn configuration for Render deployment
# Default timeout is 30s — Gemini 2.5-flash can take 40-60s → SIGKILL
# Increasing to 120s fixes the "Worker was sent SIGKILL" error

timeout = 120          # seconds before worker is killed (default: 30)
workers = 1            # free tier has limited RAM — keep at 1
worker_class = "sync"  # sync is fine for Django
