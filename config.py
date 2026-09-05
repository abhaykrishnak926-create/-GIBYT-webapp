import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def _normalize_database_url(raw_url):
    if not raw_url:
        return raw_url
    if raw_url.startswith("postgres://"):
        return raw_url.replace("postgres://", "postgresql+psycopg://", 1)
    if raw_url.startswith("postgresql://") and "+psycopg" not in raw_url:
        return raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return raw_url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY is not set. Copy .env.example to .env and fill it in."
        )

    SQLALCHEMY_DATABASE_URI = _normalize_database_url(os.environ.get("DATABASE_URL"))
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy .env.example to .env and fill it in."
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REMEMBER_COOKIE_DURATION = timedelta(days=14)

    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"
    REMEMBER_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"
    SESSION_COOKIE_HTTPONLY = True