from app.services.geocoding_service import geocode
from app.clients.weather_client import fetch_weather
from app.clients.weather_client import fetch_forecast
from collections import defaultdict
from datetime import datetime, timezone

def get_weather(location: str):
    loc = geocode(location)

    data = fetch_weather(loc["lat"], loc["lon"])

    return {
        "city": loc["city"] or data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
    }


def format_forecast(data, loc):
    days = defaultdict(list)

    # Group by day
    for item in data["list"]:
        day = datetime.fromtimestamp(item["dt"], tz=timezone.utc).strftime("%Y-%m-%d")
        days[day].append(item)

    forecast = []

    for day, entries in list(days.items())[:5]:
        temps = [e["main"]["temp"] for e in entries]

        forecast.append({
            "date": day,
            "temp_min": min(temps),
            "temp_max": max(temps),
            "description": entries[0]["weather"][0]["description"],
        })

    return {
        "city": loc["city"],
        "country": loc["country"],
        "forecast": forecast
    }


def get_forecast(location: str):
    loc = geocode(location)

    raw = fetch_forecast(loc["lat"], loc["lon"])

    return format_forecast(raw, loc)