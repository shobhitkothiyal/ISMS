import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_key_123"
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        'mysql+mysqlconnector://admin:ZLwDR01PKKvO9cd6B6iJ@isms1.c29e48ws2cbo.us-east-1.rds.amazonaws.com/isms1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Storage Configuration
    SCREENSHOT_FOLDER = os.path.join(BASE_DIR, "storage", "screenshots")
    
    DEBUG = True

