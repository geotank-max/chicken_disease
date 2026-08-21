import os 
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    
    # Set DATABASE_URL to override (e.g., use SQLite in dev); default is PostgreSQL.
    SQLALCHEMY_DATABASE_URI = (os.environ.get("DATABASE_URL") 
        or f"postgresql://{os.environ.get('DB_USER', 'postgres')}:{os.environ.get('DB_PASSWORD', '123456789')}@{os.environ.get('DB_HOST', 'localhost')}:{os.environ.get('DB_PORT', '5432')}/{os.environ.get('DB_NAME', 'chicken_diagnoses')}")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
