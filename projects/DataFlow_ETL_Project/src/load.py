import sqlite3
from src.config import DB_PATH

def load_to_warehouse(weather_df, world_bank_df):
    with sqlite3.connect(DB_PATH) as conn:
        weather_df.to_sql("weather_daily", conn, if_exists="replace", index=False)
        world_bank_df.to_sql("world_bank_indicator", conn, if_exists="replace", index=False)
        conn.execute("""CREATE TABLE IF NOT EXISTS etl_run_log (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            completed_at TEXT DEFAULT CURRENT_TIMESTAMP,
            weather_rows INTEGER,
            world_bank_rows INTEGER,
            status TEXT
        )""")
        conn.execute(
            "INSERT INTO etl_run_log (weather_rows, world_bank_rows, status) VALUES (?, ?, ?)",
            (len(weather_df), len(world_bank_df), "SUCCESS")
        )
    return DB_PATH
