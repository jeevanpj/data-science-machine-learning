from src.transform import transform_weather, transform_world_bank

def test_transform_weather():
    payload = {"daily": {
        "time": ["2026-01-01", "2026-01-02"],
        "temperature_2m_max": [30, 31],
        "temperature_2m_min": [20, 21],
        "precipitation_sum": [0, 1.5],
    }}
    result = transform_weather(payload)
    assert len(result) == 2
    assert "temperature_range_c" in result.columns

def test_transform_world_bank():
    payload = [{"pages": 1}, [{
        "countryiso3code": "IND", "country": {"value": "India"}, "date": "2024",
        "indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP"}, "value": 100.0
    }]]
    result = transform_world_bank(payload)
    assert len(result) == 1
    assert result.iloc[0]["year"] == 2024
