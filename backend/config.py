import os
from urllib.parse import quote_plus

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

_DB_USER     = os.environ.get("DB_USER")     or "naman"
_DB_PASSWORD = os.environ.get("DB_PASSWORD") or "Naman@#123"
_DB_HOST     = os.environ.get("DB_HOST")     or "93.127.199.4"
_DB_NAME     = os.environ.get("DB_NAME")     or "isms"

# ✅ FIX: URL-encode the password so special chars like @ and # don't break the URI parser
_DB_PASSWORD_ENCODED = quote_plus(_DB_PASSWORD)

_DB_URI = f"mysql+mysqlconnector://{_DB_USER}:{_DB_PASSWORD_ENCODED}@{_DB_HOST}/{_DB_NAME}"

print(f"[config.py] DB URI => {_DB_URI}")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_key_123"

    DB_USER     = _DB_USER
    DB_PASSWORD = _DB_PASSWORD
    DB_HOST     = _DB_HOST
    DB_NAME     = _DB_NAME

    SQLALCHEMY_DATABASE_URI        = _DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ================= STORAGE =================
    SCREENSHOT_FOLDER = os.path.join(BASE_DIR, "storage", "screenshots")

    # ================= DEBUG =================
    DEBUG = True