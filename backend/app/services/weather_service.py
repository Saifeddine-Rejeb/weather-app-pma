from app.clients.weather_client import fetch_weather

def get_weather(city):
    data = fetch_weather(city)

    return {
        "city": data.get("name"),
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"]
    }