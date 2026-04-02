import os
from typing import Optional

def env(name, default=None):
    return os.getenv(name, default)


def env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


class Config:
    # Flask config
    # In production, set SECRET_KEY in the environment.
    # For local/dev, we generate a random key at runtime if not provided.
    SECRET_KEY = env("SECRET_KEY")
    if not SECRET_KEY:
        SECRET_KEY = os.urandom(32)

    # Database config (from environment variables)
    DB_HOST = env("DB_HOST", "localhost")
    DB_USER = env("DB_USER", "airuser")
    DB_PASSWORD = env("DB_PASSWORD", "")
    DB_NAME = env("DB_NAME", "air")

    # SQLAlchemy config
    DATABASE_URL = env("DATABASE_URL")
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Other config
    # Default SAFE: False unless explicitly enabled.
    DEBUG = env_bool("FLASK_DEBUG", False) or env_bool("DEBUG", False)