import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
from src.config import DB_PATH, LOCATION_NAME

st.set_page_config(page_title="DataFlow | ETL Monitor", page_icon="🔄", layout="wide")
st.title("DataFlow — ETL Analytics Dashboard")
st.caption("Open-Meteo + World Bank API | SQLite warehouse")

if not DB_PATH.exists():
    st.warning("Warehouse not found. Run `python -m src.pipeline` from the project root first.")
    st.stop()

with sqlite3.connect(DB_PATH) as conn:
    weather = pd.read_sql_query("SELECT * FROM weather_daily ORDER BY date", conn)
    wb = pd.read_sql_query("SELECT * FROM world_bank_indicator ORDER BY year", conn)
    logs = pd.read_sql_query("SELECT * FROM etl_run_log ORDER BY run_id DESC", conn)

a, b, c = st.columns(3)
a.metric("Weather records", len(weather))
b.metric("Economic indicator records", len(wb))
c.metric("Location", LOCATION_NAME)

st.subheader("Weather")
if not weather.empty:
    weather["date"] = pd.to_datetime(weather["date"])
    st.plotly_chart(px.line(weather, x="date", y=["temperature_max_c", "temperature_min_c"],
                            markers=True, title="Daily maximum and minimum temperature"),
                    use_container_width=True)
    st.dataframe(weather, use_container_width=True)
else:
    st.info("No weather records found.")

st.subheader("World Bank indicator")
if not wb.empty:
    valid = wb.dropna(subset=["value"]).sort_values("year")
    if not valid.empty:
        st.plotly_chart(px.line(valid, x="year", y="value", markers=True,
                                title=valid["indicator_name"].iloc[0] or "Indicator trend"),
                        use_container_width=True)
    st.dataframe(wb, use_container_width=True)
else:
    st.info("No economic indicator records found.")

st.subheader("ETL run history")
st.dataframe(logs, use_container_width=True)
