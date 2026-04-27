import os
import requests
from app.exceptions import WeatherClientError

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"
AQI_URL = "https://api.openweathermap.org/data/2.5/air_pollution"


def _get(url, params, timeout=5):
    """Shared GET helper with consistent error handling."""
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        raise WeatherClientError(f"Request to {url} timed out.")
    except requests.HTTPError as e:
        raise WeatherClientError(
            f"Weather API error: {e.response.status_code} {e.response.text}"
        )
    except requests.RequestException as e:
        raise WeatherClientError(f"Request failed: {str(e)}")


def fetch_weather(lat: float, lon: float) -> dict:
    return _get(
        BASE_URL + "/weather",
        {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"},
    )


def fetch_forecast(lat: float, lon: float) -> dict:
    return _get(
        BASE_URL + "/forecast",
        {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"},
    )


def fetch_air_quality(lat: float, lon: float) -> dict:
    return _get(
        AQI_URL,
        {"lat": lat, "lon": lon, "appid": API_KEY},
    )
