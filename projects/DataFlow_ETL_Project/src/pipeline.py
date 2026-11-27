from src.extract import run_extraction
from src.transform import transform_weather, transform_world_bank, save_processed
from src.load import load_to_warehouse

def main():
    print("\\n========== DATAFLOW ETL STARTED ==========")
    weather_raw, world_bank_raw = run_extraction()
    print("\\nTransforming data...")
    weather_df = transform_weather(weather_raw)
    world_bank_df = transform_world_bank(world_bank_raw)
    save_processed(weather_df, world_bank_df)
    print("\\nLoading data into warehouse...")
    db_path = load_to_warehouse(weather_df, world_bank_df)
    print("\\n========== ETL COMPLETED ==========")
    print(f"Weather rows: {len(weather_df)}")
    print(f"World Bank rows: {len(world_bank_df)}")
    print(f"Warehouse: {db_path}")
    return weather_df, world_bank_df

if __name__ == "__main__":
    main()
