"""Central configuration. Values come from the .env file (see .env.example)."""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "placement_model.joblib"
DB_BACKEND = os.getenv("DB_BACKEND", "sqlite").lower()          # "sqlite" or "mysql"
SQLITE_PATH = os.getenv("SQLITE_PATH", str(ROOT / "career_ai.db"))
MYSQL = dict(host=os.getenv("DB_HOST", "localhost"), port=int(os.getenv("DB_PORT", "3306")),
             user=os.getenv("DB_USER", "root"), password=os.getenv("DB_PASSWORD", ""),
             database=os.getenv("DB_NAME", "career_ai"))

# ---- About / author info (edit these in your .env file) ----
AUTHOR = dict(
    name=os.getenv("AUTHOR_NAME", "Ankit"),
    email=os.getenv("AUTHOR_EMAIL", "ankitchadrabad9389@gmail.com"),
    github=os.getenv("AUTHOR_GITHUB", "https://github.com/your-username"),
    linkedin=os.getenv("AUTHOR_LINKEDIN", "https://www.linkedin.com/in/ankit-b47699332"),
    college=os.getenv("AUTHOR_COLLEGE", "B.Tech CSE (Final Year)"),
)
