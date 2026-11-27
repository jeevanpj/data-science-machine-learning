
import sys
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# --------------------------------------------------
# 1. PROJECT PATH CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.config import DB_PATH, LOCATION_NAME


# --------------------------------------------------
# 2. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="DataFlow | ETL Analytics",
    page_icon="🔄",
    layout="wide"
)

st.title("🔄 DataFlow — ETL Analytics Dashboard")

st.caption(
    "Automated Data Engineering Pipeline | "
    "Open-Meteo API + World Bank API | SQLite Warehouse"
)


# --------------------------------------------------
# 3. DATABASE INITIALIZATION
# --------------------------------------------------

if not DB_PATH.exists():

    st.info("Data warehouse not found. Initializing DataFlow...")

    try:
        with st.spinner("Extracting, transforming and loading data..."):

            from src.pipeline import main

            main()

        st.success("Data warehouse created successfully!")

        st.rerun()

    except Exception as e:
        st.error(f"Pipeline initialization failed: {e}")
        st.stop()


# --------------------------------------------------
# 4. LOAD DATABASE TABLES
# --------------------------------------------------

try:

    with sqlite3.connect(DB_PATH) as conn:

        weather = pd.read_sql_query(
            "SELECT * FROM weather_daily ORDER BY date",
            conn
        )

        wb = pd.read_sql_query(
            "SELECT * FROM world_bank_indicator ORDER BY year",
            conn
        )

        logs = pd.read_sql_query(
            "SELECT * FROM etl_run_log ORDER BY run_id DESC",
            conn
        )

except Exception as e:

    st.error(f"Unable to read warehouse data: {e}")
    st.stop()


# --------------------------------------------------
# 5. DASHBOARD METRICS
# --------------------------------------------------

st.subheader("Pipeline Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Weather Records",
    len(weather)
)

col2.metric(
    "Economic Records",
    len(wb)
)

col3.metric(
    "Location",
    LOCATION_NAME
)

st.divider()


# --------------------------------------------------
# 6. WEATHER ANALYTICS
# --------------------------------------------------

st.subheader("🌤️ Weather Analytics")

if not weather.empty:

    weather["date"] = pd.to_datetime(weather["date"])

    st.plotly_chart(
        px.line(
            weather,
            x="date",
            y=[
                "temperature_max_c",
                "temperature_min_c"
            ],
            markers=True,
            title="Daily Maximum and Minimum Temperature",
            labels={
                "date": "Date",
                "value": "Temperature (°C)",
                "variable": "Temperature Type"
            }
        ),
        use_container_width=True
    )

    st.markdown("**Weather Dataset**")

    st.dataframe(
        weather,
        use_container_width=True
    )

else:

    st.info("No weather records available.")


st.divider()


# --------------------------------------------------
# 7. WORLD BANK ECONOMIC ANALYTICS
# --------------------------------------------------

st.subheader("🌍 World Bank Economic Analytics")

if not wb.empty:

    valid = wb.dropna(subset=["value"]).sort_values("year")

    if not valid.empty:

        indicator_title = (
            valid["indicator_name"].iloc[0]
            or "World Bank Indicator Trend"
        )

        st.plotly_chart(
            px.line(
                valid,
                x="year",
                y="value",
                markers=True,
                title=indicator_title,
                labels={
                    "year": "Year",
                    "value": "Indicator Value"
                }
            ),
            use_container_width=True
        )

    st.markdown("**Economic Dataset**")

    st.dataframe(
        wb,
        use_container_width=True
    )

else:

    st.info("No economic records available.")


st.divider()


# --------------------------------------------------
# 8. ETL EXECUTION HISTORY
# --------------------------------------------------

st.subheader("⚙️ ETL Pipeline Execution History")

if not logs.empty:

    st.dataframe(
        logs,
        use_container_width=True
    )

else:

    st.info("No pipeline execution history available.")


# --------------------------------------------------
# 9. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "DataFlow | API-Based ETL Pipeline | "
    "Python • Pandas • SQLite • Streamlit • Plotly"
)
