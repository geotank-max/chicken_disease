import os 

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
    
    # Build database URL from components
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
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
