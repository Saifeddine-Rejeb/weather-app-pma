import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(lat, lon):
    response = requests.get(
        BASE_URL,
        params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"},
    )

    return response.json()
