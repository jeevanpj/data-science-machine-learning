import sys
import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st
import plotly.express as px

# --------------------------------------------------
# Project imports
# --------------------------------------------------
PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.config import DB_PATH, LOCATION_NAME


# --------------------------------------------------
# Page configuration and styling
# --------------------------------------------------
st.set_page_config(
    page_title="DataFlow | ETL Analytics",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .block-container {padding-top: 2rem; padding-bottom: 2rem;}
      [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(45, 55, 72, .55), rgba(30, 41, 59, .35));
        border: 1px solid rgba(148, 163, 184, .22);
        padding: 18px 20px;
        border-radius: 14px;
      }
      div[data-testid="stButton"] > button {
        border-radius: 10px;
        min-height: 2.8rem;
        font-weight: 600;
      }
      .section-note {color: #94a3b8; font-size: .92rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔄 DataFlow")
st.caption("API-powered ETL pipeline · Weather + World Bank economic indicators")


# --------------------------------------------------
# Pipeline controls
# --------------------------------------------------
with st.sidebar:
    st.header("Pipeline controls")
    st.markdown(
        '<p class="section-note">Extract fresh API data, transform it, and load it into the SQLite warehouse.</p>',
        unsafe_allow_html=True,
    )
    run_pipeline = st.button("▶ Run ETL Pipeline", type="primary", use_container_width=True)
    st.divider()
    st.caption(f"Configured location: **{LOCATION_NAME}**")
    st.caption("Sources: Open-Meteo API · World Bank API")
    st.caption("Storage: SQLite")

if run_pipeline:
    try:
        with st.spinner("Running extraction, transformation and loading..."):
            from src.pipeline import main
            main()
        st.success("ETL pipeline completed successfully. Dashboard data refreshed.")
        st.rerun()
    except Exception as exc:
        st.error(f"ETL pipeline failed: {exc}")
        st.exception(exc)


# --------------------------------------------------
# Ensure warehouse exists on first cloud startup
# --------------------------------------------------
if not DB_PATH.exists():
    st.info("The warehouse has not been created in this app session. Running the initial ETL pipeline...")
    try:
        with st.spinner("Initializing the data warehouse from the public APIs..."):
            from src.pipeline import main
            main()
        st.success("Initial data load completed.")
        st.rerun()
    except Exception as exc:
        st.error(f"Could not initialize the data warehouse: {exc}")
        st.exception(exc)
        st.stop()


# --------------------------------------------------
# Load warehouse tables
# --------------------------------------------------
try:
    with sqlite3.connect(DB_PATH) as conn:
        weather = pd.read_sql_query(
            "SELECT * FROM weather_daily ORDER BY date", conn
        )
        world_bank = pd.read_sql_query(
            "SELECT * FROM world_bank_indicator ORDER BY year", conn
        )
        logs = pd.read_sql_query(
            "SELECT * FROM etl_run_log ORDER BY run_id DESC", conn
        )
except Exception as exc:
    st.error(f"Unable to read the SQLite warehouse: {exc}")
    st.exception(exc)
    st.stop()


# --------------------------------------------------
# Overview metrics
# --------------------------------------------------
st.subheader("Pipeline overview")
metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric("Weather records", f"{len(weather):,}")
metric2.metric("Economic records", f"{len(world_bank):,}")
metric3.metric("ETL runs", f"{len(logs):,}")
last_run = logs.iloc[0]["completed_at"] if not logs.empty else "Not available"
metric4.metric("Last successful run", str(last_run))

st.divider()


# --------------------------------------------------
# Weather analytics
# --------------------------------------------------
st.subheader("🌤️ Weather analytics")
st.caption("Daily forecast and recent observations retrieved from Open-Meteo.")

if not weather.empty:
    weather["date"] = pd.to_datetime(weather["date"], errors="coerce")
    weather = weather.dropna(subset=["date"]).sort_values("date")

    if {"temperature_max_c", "temperature_min_c"}.issubset(weather.columns):
        weather_chart = px.line(
            weather,
            x="date",
            y=["temperature_max_c", "temperature_min_c"],
            markers=True,
            title="Daily maximum and minimum temperature",
            labels={
                "date": "Date",
                "value": "Temperature (°C)",
                "variable": "Measure",
            },
            template="plotly_dark",
        )
        weather_chart.update_layout(legend_title_text="Temperature")
        st.plotly_chart(weather_chart, use_container_width=True)

    if "precipitation_mm" in weather.columns:
        rain_chart = px.bar(
            weather,
            x="date",
            y="precipitation_mm",
            title="Daily precipitation",
            labels={"date": "Date", "precipitation_mm": "Precipitation (mm)"},
            template="plotly_dark",
        )
        st.plotly_chart(rain_chart, use_container_width=True)

    with st.expander("View weather source data"):
        st.dataframe(weather, use_container_width=True, hide_index=True)
else:
    st.info("No weather records are currently available.")


st.divider()


# --------------------------------------------------
# World Bank analytics
# --------------------------------------------------
st.subheader("🌍 World Bank economic indicator")
st.caption("Historical economic indicator data retrieved from the World Bank API.")

if not world_bank.empty:
    valid = world_bank.dropna(subset=["value", "year"]).sort_values("year")

    if not valid.empty:
        indicator_name = valid["indicator_name"].iloc[0] or "Economic indicator"
        economic_chart = px.line(
            valid,
            x="year",
            y="value",
            markers=True,
            title=indicator_name,
            labels={"year": "Year", "value": "Indicator value"},
            template="plotly_dark",
        )
        st.plotly_chart(economic_chart, use_container_width=True)

        latest = valid.iloc[-1]
        st.metric(
            f"Latest available value · {int(latest['year'])}",
            f"{latest['value']:,.2f}",
        )
    else:
        st.info("The World Bank API returned records, but no numeric indicator values are available.")

    with st.expander("View World Bank source data"):
        st.dataframe(world_bank, use_container_width=True, hide_index=True)
else:
    st.info("No economic indicator records are currently available.")


st.divider()


# --------------------------------------------------
# ETL execution history
# --------------------------------------------------
st.subheader("🧾 ETL execution history")
if not logs.empty:
    st.dataframe(logs, use_container_width=True, hide_index=True)
else:
    st.info("No ETL execution history is available yet.")


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()
st.caption(
    "DataFlow · Python · Requests · Pandas · SQLite · Streamlit · Plotly"
)
