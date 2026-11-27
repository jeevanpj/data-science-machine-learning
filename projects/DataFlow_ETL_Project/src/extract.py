import json
import requests
from src.config import LATITUDE, LONGITUDE, LOCATION_NAME, TIMEZONE
from src.config import WORLD_BANK_COUNTRY, WORLD_BANK_INDICATOR, RAW_DIR

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "DataFlow-Educational-ETL/1.0"})

def save_json(data, filename):
    path = RAW_DIR / filename
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path

def extract_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": TIMEZONE,
        "past_days": 7,
        "forecast_days": 7,
    }
    response = SESSION.get(url, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    save_json(payload, "weather_raw.json")
    print(f"Weather response received for {LOCATION_NAME}.")
    return payload

def extract_world_bank():
    url = f"https://api.worldbank.org/v2/country/{WORLD_BANK_COUNTRY}/indicator/{WORLD_BANK_INDICATOR}"
    response = SESSION.get(url, params={"format": "json", "per_page": 100}, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        raise ValueError(f"Unexpected World Bank API response: {payload}")
    save_json(payload, "world_bank_raw.json")
    print(f"World Bank records received: {len(payload[1])}.")
    return payload

def run_extraction():
    print("Extracting weather data...")
    weather = extract_weather()
    print("Extracting World Bank indicator data...")
    world_bank = extract_world_bank()
    return weather, world_bank
