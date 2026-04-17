from app.services.geocoding_service import geocode
from app.clients.weather_client import fetch_weather


def get_weather(location: str):
    loc = geocode(location)

    data = fetch_weather(loc["lat"], loc["lon"])

    return {
        "city": loc["city"] or data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
    }
