import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"


def fetch_weather(lat, lon):
    response = requests.get(
        BASE_URL + "/weather",
        params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"},
    )

    return response.json()

def fetch_forecast(lat, lon):

    response = requests.get(
        BASE_URL + "/forecast",
        params={
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric"
        },
        timeout=5
    )

    response.raise_for_status()
    return response.json()