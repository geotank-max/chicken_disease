import os 
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    # ── Session cookie settings ──────────────────────────────────
    # SameSite=Lax lets the session cookie (which carries the OAuth
    # "state" value) survive the top-level redirect coming back from
    # Google. Without this the cookie can be dropped on the first
    # attempt, causing a state mismatch that only succeeds on retry
    # once the cookie has been established.
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True
    # Set to True in production (HTTPS). Kept False so it also works
    # over plain http://localhost during development.
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() in ("true", "1", "yes")
    # Keep the user signed in after closing/reopening the browser so
    # they return to the same account. Applies when session.permanent
    # is set on login. Default: 7 days.
    from datetime import timedelta as _timedelta
    PERMANENT_SESSION_LIFETIME = _timedelta(
        days=int(os.environ.get("SESSION_LIFETIME_DAYS", "7"))
    )

    # Flask-Login "remember me" cookie: keeps the user on the same
    # account after closing/reopening the browser. Mirror the session
    # cookie security settings.
    REMEMBER_COOKIE_DURATION = _timedelta(
        days=int(os.environ.get("SESSION_LIFETIME_DAYS", "7"))
    )
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() in ("true", "1", "yes")

    # Upload config
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024   # 50 MB total request cap
    MAX_FORM_MEMORY_SIZE = 50 * 1024 * 1024  # allow large files in multipart memory buffer

    # PostgreSQL Connection Details
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "123")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "chicken_diagnoses")
    
    # Set DATABASE_URL to override (e.g., managed DB in production).
    # Otherwise build the URL from the individual DB_* components above.
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Email / SMTP settings ────────────────────────────────────
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ("true", "1", "yes")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

    # ── Google OAuth / OIDC ───────────────────────────────────────
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:5000/auth/google/callback")
