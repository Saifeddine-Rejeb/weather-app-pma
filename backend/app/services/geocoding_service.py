import os
import requests
from app.exceptions import GeocodingError

API_KEY = os.getenv("WEATHER_API_KEY")
GEO_BASE = "https://api.openweathermap.org/geo/1.0"


def is_coords(location: str) -> bool:
    """Detect 'lat,lon' format."""
    try:
        parts = location.split(",")
        if len(parts) != 2:
            return False
        float(parts[0].strip())
        float(parts[1].strip())
        return True
    except (ValueError, AttributeError):
        return False


def is_zip(location: str) -> bool:
    """Detect zip/postal code — alphanumeric with at least one digit."""
    stripped = location.replace(" ", "").replace("-", "")
    return (
        stripped.isalnum()
        and any(c.isdigit() for c in stripped)
        and len(stripped) <= 10
    )


def parse_coords(location: str) -> dict:
    parts = location.split(",")
    return {
        "lat": float(parts[0].strip()),
        "lon": float(parts[1].strip()),
        "city": None,
        "country": None,
    }


def geocode_zip(location: str) -> dict | None:
    """Try OpenWeather zip geocoding. Returns None if not found."""
    try:
        resp = requests.get(
            f"{GEO_BASE}/zip",
            params={"zip": location, "appid": API_KEY},
            timeout=5,
        )
        if resp.status_code != 200:
            return None
        d = resp.json()
        if "lat" not in d:
            return None
        return {
            "lat": d["lat"],
            "lon": d["lon"],
            "city": d.get("name"),
            "country": d.get("country"),
        }
    except requests.RequestException:
        return None


def geocode_text(location: str) -> dict:
    """Geocode a free-text location name. Raises GeocodingError if nothing found."""
    try:
        resp = requests.get(
            f"{GEO_BASE}/direct",
            params={"q": location, "limit": 1, "appid": API_KEY},
            timeout=5,
        )
        resp.raise_for_status()
        results = resp.json()
    except requests.Timeout:
        raise GeocodingError(f"Geocoding request timed out for: {location}")
    except requests.RequestException as e:
        raise GeocodingError(f"Geocoding request failed: {str(e)}")

    if not results:
        raise GeocodingError(f"Location not found: '{location}'")

    d = results[0]
    return {
        "lat": d["lat"],
        "lon": d["lon"],
        "city": d.get("name"),
        "country": d.get("country"),
    }


def geocode(location: str) -> dict:
    """
    Resolve any location string to {lat, lon, city, country}.
    Strategy: coordinates → zip code → free text.
    Raises GeocodingError if all strategies fail.
    """
    location = location.strip()

    if not location:
        raise GeocodingError("Location cannot be empty.")

    if is_coords(location):
        return parse_coords(location)

    if is_zip(location):
        result = geocode_zip(location)
        if result:
            return result
        # Fall through to text if zip returned nothing

    return geocode_text(location)
