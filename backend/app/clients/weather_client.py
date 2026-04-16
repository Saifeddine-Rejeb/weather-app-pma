import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")


def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()
