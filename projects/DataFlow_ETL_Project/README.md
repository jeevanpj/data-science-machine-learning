# DataFlow — API-to-Warehouse ETL Project

A runnable starter project that extracts weather data from Open-Meteo and economic indicators from the World Bank API, transforms them with pandas, loads them into SQLite, and displays results in Streamlit.

## Recommended platform
Use **VS Code + Python 3.10+** for the ETL scripts and Streamlit. Use Jupyter Notebook for exploration. Airflow and Docker are planned as the next extension after this base pipeline works.

## Setup (Windows)
1. Install Python: https://www.python.org/downloads/ (select "Add Python to PATH").
2. Install VS Code: https://code.visualstudio.com/
3. Extract this ZIP and open the `DataFlow_ETL_Project` folder in VS Code.
4. Open Terminal > New Terminal and run:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Copy `.env.example` to `.env`. The included public APIs do not require API keys.
6. Run the complete ETL pipeline from the project root:

```powershell
python -m src.pipeline
```

This creates raw JSON files, cleaned CSV files and `data/warehouse.db`.

7. Start the dashboard:

```powershell
streamlit run app/streamlit_app.py
```

Open the local URL printed in the terminal, usually http://localhost:8501.

8. Optional tests:

```powershell
pytest -q
```

## Jupyter option
Install Jupyter with `pip install jupyter`, run `jupyter notebook`, and open `notebooks/DataFlow_Exploration.ipynb`. Run the ETL pipeline from the project root first.

## Data sources
- Open-Meteo: https://open-meteo.com/
- World Bank Indicators API: https://api.worldbank.org/
Both example endpoints are public and do not require an API key. Their availability and terms/rate limits may change.

## Included
- `src/extract.py`: API extraction
- `src/transform.py`: cleaning and normalization
- `src/load.py`: SQLite warehouse loading
- `src/pipeline.py`: runs the ETL stages in order
- `app/streamlit_app.py`: dashboard
- `tests/`: basic transformation tests
- `notebooks/`: optional exploration notebook

## Next extensions
After the base version runs, we will add PostgreSQL, Apache Airflow scheduling, Docker, data-quality checks, retries, structured logging, incremental loads and cloud deployment. Do not commit `.env`, secrets, local database files or large raw datasets to GitHub.
