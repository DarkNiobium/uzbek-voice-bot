import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()
DEFAULT_SCRIPT = os.getenv("DEFAULT_SCRIPT", "latin").strip().lower()

if not BOT_TOKEN:
    print("[OGOHLANTIRISH] BOT_TOKEN o'rnatilmagan! .env faylini to'ldiring.")
if not GEMINI_API_KEY:
    print("[OGOHLANTIRISH] GEMINI_API_KEY o'rnatilmagan! .env faylini to'ldiring.")
