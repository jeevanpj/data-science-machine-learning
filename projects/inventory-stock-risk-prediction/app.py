import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Inventory Stock Risk Prediction", page_icon="📦", layout="wide")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "stock_risk_model.pkl")


@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


def build_features(data):
    """Create the same engineered features used during model training."""
    out = data.copy()
    out["days_of_inventory"] = out["current_stock"] / out["avg_daily_demand"].replace(0, np.nan)
    out["demand_during_lead_time"] = out["avg_daily_demand"] * out["lead_time_days"]
    out["stock_vs_reorder_ratio"] = out["current_stock"] / out["reorder_point"].replace(0, np.nan)
    out["forecast_abs_error"] = out["forecast_error"].abs()
    out["sales_per_day_30d"] = out["sales_last_30_days"] / 30
    return out


model = load_model()
st.title("📦 Inventory Stock Risk Prediction")
st.write("Estimate whether an inventory item may face stockout or overstock risk.")

if model is None:
    st.error("Trained model not found. Run the notebook to generate stock_risk_model.pkl, then place it beside app.py.")
    st.stop()

st.subheader("Enter inventory details")
col1, col2, col3 = st.columns(3)

with col1:
    current_stock = st.number_input("Current stock", min_value=0.0, value=300.0)
    avg_daily_demand = st.number_input("Average daily demand", min_value=0.01, value=40.0)
    lead_time_days = st.number_input("Lead time (days)", min_value=0.0, value=7.0)
    reorder_point = st.number_input("Reorder point", min_value=0.01, value=300.0)

with col2:
    sales_last_30_days = st.number_input("Sales in last 30 days", min_value=0.0, value=1200.0)
    stock_turnover_ratio = st.number_input("Stock turnover ratio", min_value=0.0, value=3.5)
    forecast_error = st.number_input("Forecast error", value=0.0)
    season = st.selectbox("Season", ["peak", "off-peak"])

with col3:
    item_category = st.selectbox("Item category", ["essential", "non-essential"])
    supplier_reliability = st.selectbox("Supplier reliability", ["high", "medium", "low"])

if st.button("Predict stock risk", type="primary"):
    input_data = pd.DataFrame({
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
    })
    features = build_features(input_data)
    prediction = int(model.predict(features)[0])
    class_labels = list(model.classes_)
    stockout_index = class_labels.index(1)
    stockout_probability = float(model.predict_proba(features)[0, stockout_index])

    st.subheader("Prediction")
    metric1, metric2 = st.columns(2)
    metric1.metric("Predicted stock status", "Stockout risk" if prediction == 1 else "Overstock risk")
    metric2.metric("Estimated stockout probability", f"{stockout_probability:.1%}")

    if prediction == 1:
        st.warning("Potential stockout risk. Review replenishment timing, safety stock and supplier lead time.")
    else:
        st.success("Potential overstock risk. Review purchasing quantities, demand assumptions and inventory movement.")

    st.caption("Decision-support output only. Validate predictions against current operational data and business context.")
