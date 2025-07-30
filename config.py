import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Database configuration
    BASE_DIR = Path(__file__).parent
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JSON configuration
    JSON_SORT_KEYS = False