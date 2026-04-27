from collections import defaultdict
from datetime import datetime, timezone

from app.services.geocoding_service import geocode
from app.clients.weather_client import fetch_weather, fetch_forecast, fetch_air_quality

# AQI label mapping per OpenWeather scale (1–5)
AQI_LABELS = {
    1: "Good",
    2: "Fair",
    3: "Moderate",
    4: "Poor",
    5: "Very Poor",
}


def get_weather(location: str) -> dict:
    loc = geocode(location)
    data = fetch_weather(loc["lat"], loc["lon"])

    return {
        "city": loc["city"] or data.get("name"),
        "country": loc["country"],
        "lat": loc["lat"],
        "lon": loc["lon"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "wind_speed": data["wind"]["speed"],
        "visibility": data.get("visibility"),
    }


def get_forecast(location: str) -> dict:
    loc = geocode(location)
    raw = fetch_forecast(loc["lat"], loc["lon"])
    return _format_forecast(raw, loc)


def _format_forecast(data: dict, loc: dict) -> dict:
    """
    Group 3-hour forecast entries into daily summaries.
    Returns up to 5 days with min/max temps and representative description.
    """
    days = defaultdict(list)

    for item in data["list"]:
        day = datetime.fromtimestamp(item["dt"], tz=timezone.utc).strftime("%Y-%m-%d")
        days[day].append(item)

    forecast = []
    for day, entries in list(days.items())[:5]:
        temps = [e["main"]["temp"] for e in entries]
        # Pick the midday entry for the representative description, else first
        midday = next(
            (
                e
                for e in entries
                if "12:00:00"
                in datetime.fromtimestamp(e["dt"], tz=timezone.utc).strftime("%H:%M:%S")
            ),
            entries[0],
        )
        forecast.append(
            {
                "date": day,
                "temp_min": round(min(temps), 1),
                "temp_max": round(max(temps), 1),
                "description": midday["weather"][0]["description"],
                "icon": midday["weather"][0]["icon"],
                "humidity": midday["main"]["humidity"],
            }
        )

    return {
        "city": loc["city"],
        "country": loc["country"],
        "forecast": forecast,
    }


def get_air_quality(location: str) -> dict:
    loc = geocode(location)
    data = fetch_air_quality(loc["lat"], loc["lon"])

    item = data["list"][0]
    aqi_index = item["main"]["aqi"]
    components = item["components"]

    return {
        "city": loc["city"],
        "country": loc["country"],
        "aqi": aqi_index,
        "aqi_label": AQI_LABELS.get(aqi_index, "Unknown"),
        "components": {
            "co": components.get("co"),
            "no2": components.get("no2"),
            "o3": components.get("o3"),
            "pm2_5": components.get("pm2_5"),
            "pm10": components.get("pm10"),
        },
    }
