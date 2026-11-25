# Inventory Stock Risk Prediction

A binary-classification project that predicts whether an inventory item is at risk of **stockout** or **overstock**. The aim is to help inventory and procurement teams identify items that may need replenishment or purchasing review.

## Project overview

- Dataset supplied with this project: **5,000 rows × 11 columns**
- Target: `stock_status` (`stockout` / `overstock`)
- Target distribution in the supplied dataset: 4,543 overstock (90.86%) and 457 stockout (9.14%)
- Train/test split: stratified 80/20 (4,000 training rows and 1,000 test rows)
- Final estimator saved in `stock_risk_model.pkl`: a preprocessing + **Random Forest** pipeline

## Workflow

1. Business understanding and data loading
2. Data quality checks and duplicate/target-null handling
3. Exploratory data analysis
4. Feature engineering:
   - `days_of_inventory`
   - `demand_during_lead_time`
   - `stock_vs_reorder_ratio`
   - `forecast_abs_error`
   - `sales_per_day_30d`
5. Numerical scaling and categorical one-hot encoding
6. Comparison of Logistic Regression, Decision Tree, Random Forest and Gradient Boosting
7. Randomized hyperparameter search for Random Forest
8. Final evaluation, feature importance and model persistence
9. Streamlit prediction interface

## Results recorded in the supplied notebook

The notebook's saved output reports the following final Random Forest test metrics:

| Metric | Value |
|---|---:|
| Accuracy | 1.0000 |
| Precision | 1.0000 |
| Recall | 1.0000 |
| F1-score | 1.0000 |
| ROC-AUC | 1.0000 |
| Best cross-validation F1 | 0.9973 |

The notebook also reports these Random Forest search parameters:

- `n_estimators=200`
- `min_samples_split=2`
- `min_samples_leaf=2`
- `max_depth=12`

**Interpretation caution:** these are the metrics recorded in the supplied notebook output, not a guarantee of real-world performance. Perfect test scores are unusually high and should be independently revalidated. Check for target leakage, synthetic-data patterns, duplicate/related records across splits, and performance on a genuinely external dataset before using predictions operationally.

## Repository files

- `Inventory_Stock_Risk_Prediction.ipynb` — full analysis and model-training notebook
- `app.py` — Streamlit interface
- `stock_risk_model.pkl` — serialized fitted pipeline
- `stock_risk_prediction_dataset (1).xlsx` — supplied dataset
- `requirements.txt` — Python dependencies

## Run locally

Use Python 3.10 or 3.11 for a compatible environment, then run:

```bash
python -m venv .venv
```

Activate the environment:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install packages and launch the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The notebook searches for the Excel file in a `Datasets` directory and then recursively in the project directory. Keep the dataset in this project folder (or in `Datasets/`) when running the notebook.

## Streamlit Cloud deployment

1. Push this project folder to GitHub.
2. In Streamlit Community Cloud, create an app from the repository.
3. Set the app file path to `projects/Inventory-Stock-Risk-Prediction/app.py`.
4. Ensure the model file is committed in the same project folder.
5. Deploy and test the input form with representative records.

## Limitations

- The supplied dataset has class imbalance; stockout recall is important alongside accuracy.
- Results depend on data quality, freshness and representativeness.
- The saved scikit-learn model should be loaded with the compatible version in `requirements.txt`.
- This is a portfolio demonstration, not an autonomous replenishment system. Validate predictions with domain experts and current operational data.
- Confirm that you have permission to redistribute the supplied dataset before making the repository public.

## Author

**Jeevan PJ** — Data Science & Machine Learning portfolio project.
