import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")
GEO_BASE = "https://api.openweathermap.org/geo/1.0"


def is_coords(location: str) -> bool:
    try:
        lat, lon = map(float, location.split(","))
        return True
    except:
        return False


def is_zip(location: str) -> bool:
    return location.replace(" ", "").isalnum() and any(c.isdigit() for c in location)


def parse_coords(location: str):
    lat, lon = map(float, location.split(","))
    return {
        "lat": lat,
        "lon": lon,
        "city": None,
        "country": None,
    }


def geocode_zip(location: str):
    resp = requests.get(
        f"{GEO_BASE}/zip",
        params={"zip": location, "appid": API_KEY},
        timeout=5,
    )

    if resp.status_code != 200:
        return None

    d = resp.json()
    return {
        "lat": d["lat"],
        "lon": d["lon"],
        "city": d.get("name"),
        "country": d.get("country"),
    }


def geocode_text(location: str):
    resp = requests.get(
        f"{GEO_BASE}/direct",
        params={"q": location, "limit": 1, "appid": API_KEY},
        timeout=5,
    )

    if resp.status_code != 200 or not resp.json():
        raise Exception("Could not geocode location")

    d = resp.json()[0]
    return {
        "lat": d["lat"],
        "lon": d["lon"],
        "city": d.get("name"),
        "country": d.get("country"),
    }


def geocode(location: str):
    if is_coords(location):
        return parse_coords(location)

    if is_zip(location):
        result = geocode_zip(location)
        if result:
            return result

    return geocode_text(location)
