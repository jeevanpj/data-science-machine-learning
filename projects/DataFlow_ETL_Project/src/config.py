import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

LATITUDE = float(os.getenv("LATITUDE", "12.9716"))
LONGITUDE = float(os.getenv("LONGITUDE", "77.5946"))
LOCATION_NAME = os.getenv("LOCATION_NAME", "Bengaluru")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")
WORLD_BANK_COUNTRY = os.getenv("WORLD_BANK_COUNTRY", "IND")
WORLD_BANK_INDICATOR = os.getenv("WORLD_BANK_INDICATOR", "NY.GDP.MKTP.CD")

RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
DB_PATH = ROOT_DIR / "data" / "warehouse.db"
for folder in (RAW_DIR, PROCESSED_DIR, DB_PATH.parent):
    folder.mkdir(parents=True, exist_ok=True)
