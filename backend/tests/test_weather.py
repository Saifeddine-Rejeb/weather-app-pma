import pytest
import app.services.weather_service as ws
from app.exceptions import GeocodingError, WeatherClientError

FAKE_LOC = {"lat": 36.8065, "lon": 10.1815, "city": "Tunis", "country": "TN"}

FAKE_WEATHER_DATA = {
    "name": "Tunis",
    "main": {
        "temp": 22.5,
        "feels_like": 21.0,
        "temp_min": 20.0,
        "temp_max": 24.0,
        "humidity": 60,
    },
    "weather": [{"description": "clear sky", "icon": "01d"}],
    "wind": {"speed": 5.0},
    "visibility": 10000,
}

FAKE_FORECAST_DATA = {
    "list": [
        {
            "dt": 1710000000,
            "main": {"temp": 20.0, "humidity": 55},
            "weather": [{"description": "clear sky", "icon": "01d"}],
        },
        {
            "dt": 1710086400,
            "main": {"temp": 18.0, "humidity": 60},
            "weather": [{"description": "cloudy", "icon": "03d"}],
        },
    ]
}


def test_get_weather_returns_normalized_data(monkeypatch):
    monkeypatch.setattr(ws, "geocode", lambda _: FAKE_LOC)
    monkeypatch.setattr(ws, "fetch_weather", lambda lat, lon: FAKE_WEATHER_DATA)

    result = ws.get_weather("Tunis")
    assert result["city"] == "Tunis"
    assert result["temperature"] == 22.5
    assert result["description"] == "clear sky"
    assert result["humidity"] == 60


def test_get_weather_raises_geocoding_error(monkeypatch):
    monkeypatch.setattr(
        ws, "geocode", lambda _: (_ for _ in ()).throw(GeocodingError("not found"))
    )
    with pytest.raises(GeocodingError):
        ws.get_weather("xyznonexistent")


def test_get_forecast_returns_days(monkeypatch):
    monkeypatch.setattr(ws, "geocode", lambda _: FAKE_LOC)
    monkeypatch.setattr(ws, "fetch_forecast", lambda lat, lon: FAKE_FORECAST_DATA)

    result = ws.get_forecast("Tunis")
    assert "forecast" in result
    assert len(result["forecast"]) >= 1
    assert "temp_min" in result["forecast"][0]
    assert "temp_max" in result["forecast"][0]


def test_get_air_quality_returns_aqi(monkeypatch):
    fake_aqi_data = {
        "list": [
            {
                "main": {"aqi": 2},
                "components": {"co": 200, "no2": 5, "o3": 80, "pm2_5": 10, "pm10": 15},
            }
        ]
    }
    monkeypatch.setattr(ws, "geocode", lambda _: FAKE_LOC)
    monkeypatch.setattr(ws, "fetch_air_quality", lambda lat, lon: fake_aqi_data)

    result = ws.get_air_quality("Tunis")
    assert result["aqi"] == 2
    assert result["aqi_label"] == "Fair"
    assert result["components"]["pm2_5"] == 10
