# Inventory Stock Risk Prediction

A binary-classification project that estimates whether an inventory item may face stockout or overstock risk. The objective is to support inventory and procurement teams with early risk signals.

## Project summary

- Problem: Binary classification
- Target: stock_status (stockout / overstock)
- Supplied dataset: 5,000 rows and 11 columns
- Class distribution: 4,543 overstock (90.86%) and 457 stockout (9.14%)
- Tools: Python, Pandas, NumPy, Matplotlib, Seaborn, scikit-learn, Jupyter and Streamlit

## Workflow

1. Business understanding and data loading
2. Data-quality checks and exploratory data analysis
3. Feature engineering
4. Preprocessing with scaling and one-hot encoding
5. Stratified train/test split
6. Comparison of Logistic Regression, Decision Tree, Random Forest and Gradient Boosting
7. Randomized hyperparameter search for Random Forest
8. Final evaluation, feature importance and model serialization
9. Streamlit inference application

## Project files

- Inventory_Stock_Risk_Prediction.ipynb — end-to-end analysis and model training
- app.py — Streamlit prediction interface
- requirements.txt — Python dependencies
- data/README.md — dataset placement and provenance note
- stock_risk_model.pkl — trained Random Forest model
- stock_risk_prediction_dataset (1).xlsx — Excel dataset

The dataset and trained model are included in this repository. Before redistributing the dataset further, confirm that its original source permits public sharing.

## Dataset fields

Numeric inputs: current_stock, avg_daily_demand, lead_time_days, reorder_point, sales_last_30_days, stock_turnover_ratio and forecast_error.

Categorical inputs: season, item_category and supplier_reliability.

Target: stock_status.

Place the supplied Excel workbook in this project folder or inside the data folder. The notebook includes a recursive fallback search for an Excel filename containing stock_risk.

## Results recorded in the supplied notebook

The saved notebook outputs report these metrics on its 1,000-row stratified hold-out test split:

| Metric | Reported value |
|---|---:|
| Accuracy | 1.0000 |
| Stockout precision | 1.0000 |
| Stockout recall | 1.0000 |
| Stockout F1-score | 1.0000 |
| ROC-AUC | 1.0000 |

The notebook reports a best Random Forest cross-validation F1-score of 0.9973 and uses the tuned Random Forest as the final model.

These are the results recorded in the supplied notebook, not a guarantee of performance on new or real-world inventory. The unusually high scores should be investigated for target construction, data leakage and dataset representativeness before making operational claims. Because the target is imbalanced, stockout recall and F1-score matter alongside accuracy.

## Feature engineering

The notebook creates days_of_inventory, demand_during_lead_time, stock_vs_reorder_ratio, forecast_abs_error and sales_per_day_30d. Its feature-importance output places stock_vs_reorder_ratio, current_stock, days_of_inventory and reorder_point among the leading features.

## Run locally

1. Create and activate a Python virtual environment.
2. Install dependencies with: pip install -r requirements.txt
3. Place the supplied Excel dataset in this project folder or the data folder.
4. Open the notebook and run all cells from top to bottom. This creates stock_risk_model.pkl.
5. Start the application with: streamlit run app.py

The supplied model was serialized with scikit-learn 1.7.2; the requirements file pins that version for compatibility.

## Live application

Try the deployed Streamlit application: [Inventory Stock Risk Prediction](https://data-science-machine-learning-fznu5w5wlnbwajtyz6tvn4.streamlit.app/).

## Deployment

The application is hosted on Streamlit Community Cloud and is connected to this GitHub repository. The trained `stock_risk_model.pkl` file is stored beside `app.py`, as required by the app's model-loading code.

## Limitations

- The supplied dataset has 5,000 observations and may not represent all inventory operations.
- Predictions depend on input quality and changing demand patterns.
- Perfect hold-out metrics warrant further leakage and validation checks.
- Predictions are decision-support signals, not automatic purchasing instructions.
- Evaluate on genuinely unseen, time-separated operational data before production use.

## Author

Jeevan PJ — Data Science and Machine Learning portfolio project.
