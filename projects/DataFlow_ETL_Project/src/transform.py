import pandas as pd
from src.config import LOCATION_NAME, PROCESSED_DIR, WORLD_BANK_COUNTRY, WORLD_BANK_INDICATOR

def transform_weather(payload):
    daily = payload.get("daily", {})
    required = ["time", "temperature_2m_max", "temperature_2m_min", "precipitation_sum"]
    missing = [key for key in required if key not in daily]
    if missing:
        raise ValueError(f"Weather payload is missing fields: {missing}")
    df = pd.DataFrame({
        "date": daily["time"],
        "temperature_max_c": daily["temperature_2m_max"],
        "temperature_min_c": daily["temperature_2m_min"],
        "precipitation_mm": daily["precipitation_sum"],
    })
    df["location"] = LOCATION_NAME
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["temperature_max_c", "temperature_min_c", "precipitation_mm"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["date"]).drop_duplicates(subset=["date", "location"])
    df["temperature_range_c"] = df["temperature_max_c"] - df["temperature_min_c"]
    return df

def transform_world_bank(payload):
    records = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
    rows = []
    for item in records or []:
        rows.append({
            "country_code": item.get("countryiso3code") or WORLD_BANK_COUNTRY,
            "country": (item.get("country") or {}).get("value"),
            "year": pd.to_numeric(item.get("date"), errors="coerce"),
            "indicator_code": (item.get("indicator") or {}).get("id") or WORLD_BANK_INDICATOR,
            "indicator_name": (item.get("indicator") or {}).get("value"),
            "value": pd.to_numeric(item.get("value"), errors="coerce"),
        })
    columns = ["country_code", "country", "year", "indicator_code", "indicator_name", "value"]
    df = pd.DataFrame(rows, columns=columns)
    if df.empty:
        return df
    df = df.dropna(subset=["year"]).drop_duplicates(subset=["country_code", "year", "indicator_code"])
    df["year"] = df["year"].astype(int)
    return df.sort_values("year")

def save_processed(weather_df, world_bank_df):
    weather_df.to_csv(PROCESSED_DIR / "weather_clean.csv", index=False)
    world_bank_df.to_csv(PROCESSED_DIR / "world_bank_clean.csv", index=False)
