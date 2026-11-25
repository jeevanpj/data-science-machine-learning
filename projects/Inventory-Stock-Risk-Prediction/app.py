import os

import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Inventory Stock Risk Prediction",
    page_icon="📦",
    layout="wide",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "stock_risk_model.pkl")


@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


model = load_model()

st.title("📦 Inventory Stock Risk Prediction")
st.write(
    "Estimate whether an inventory item may face **stockout** or "
    "**overstock** risk using the trained machine learning pipeline."
)

if model is None:
    st.error(
        "Model file not found. Place stock_risk_model.pkl in the same "
        "folder as app.py."
    )
    st.stop()

st.info(
    "This is a portfolio demonstration. Review model limitations and "
    "validate predictions against current operational data."
)

st.subheader("Enter inventory details")

col1, col2, col3 = st.columns(3)

with col1:
    current_stock = st.number_input("Current Stock", min_value=0.0, value=300.0)
    avg_daily_demand = st.number_input(
        "Average Daily Demand", min_value=0.01, value=40.0
    )
    lead_time_days = st.number_input("Lead Time (days)", min_value=0.0, value=7.0)
    reorder_point = st.number_input("Reorder Point", min_value=0.01, value=300.0)

with col2:
    sales_last_30_days = st.number_input(
        "Sales Last 30 Days", min_value=0.0, value=1200.0
    )
    stock_turnover_ratio = st.number_input(
        "Stock Turnover Ratio", min_value=0.0, value=3.5
    )
    forecast_error = st.number_input("Forecast Error", value=0.0)
    season = st.selectbox("Season", ["peak", "off-peak"])

with col3:
    item_category = st.selectbox(
        "Item Category", ["essential", "non-essential"]
    )
    supplier_reliability = st.selectbox(
        "Supplier Reliability", ["high", "medium", "low"]
    )

if st.button("Predict Stock Risk", type="primary"):
    input_data = pd.DataFrame(
        {
            "current_stock": [current_stock],
            "avg_daily_demand": [avg_daily_demand],
            "lead_time_days": [lead_time_days],
            "reorder_point": [reorder_point],
            "sales_last_30_days": [sales_last_30_days],
            "stock_turnover_ratio": [stock_turnover_ratio],
            "forecast_error": [forecast_error],
            "season": [season],
            "item_category": [item_category],
            "supplier_reliability": [supplier_reliability],
        }
    )

    # Keep feature engineering identical to the training notebook.
    input_data["days_of_inventory"] = (
        input_data["current_stock"]
        / input_data["avg_daily_demand"].replace(0, np.nan)
    )
    input_data["demand_during_lead_time"] = (
        input_data["avg_daily_demand"] * input_data["lead_time_days"]
    )
    input_data["stock_vs_reorder_ratio"] = (
        input_data["current_stock"]
        / input_data["reorder_point"].replace(0, np.nan)
    )
    input_data["forecast_abs_error"] = input_data["forecast_error"].abs()
    input_data["sales_per_day_30d"] = input_data["sales_last_30_days"] / 30

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    classes = list(model.classes_)
    stockout_index = classes.index(1)
    stockout_probability = probabilities[stockout_index]

    st.subheader("Prediction result")
    st.metric("Estimated Stockout Probability", f"{stockout_probability:.1%}")

    if prediction == 1:
        st.error("⚠️ Predicted status: STOCKOUT RISK")
        st.write(
            "Suggested review: replenishment timing, safety stock and "
            "supplier lead time."
        )
    else:
        st.success("Predicted status: OVERSTOCK")
        st.write(
            "Suggested review: purchasing quantity, demand assumptions "
            "and inventory movement."
        )
