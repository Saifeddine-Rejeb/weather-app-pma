import os
import requests
from app.exceptions import ExternalAPIError

MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"


def fetch_maps_data(query: str) -> dict:
    """
    Search Google Places for a location query.
    Returns a structured result with map embed link and place details.
    """
    if not MAPS_API_KEY:
        raise ExternalAPIError("GOOGLE_MAPS_API_KEY is not set.")

    try:
        response = requests.get(
            PLACES_URL,
            params={"query": query, "key": MAPS_API_KEY},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
    except requests.Timeout:
        raise ExternalAPIError("Google Maps API request timed out.")
    except requests.HTTPError as e:
        raise ExternalAPIError(f"Google Maps API error: {e.response.status_code}")
    except requests.RequestException as e:
        raise ExternalAPIError(f"Google Maps request failed: {str(e)}")

    results = data.get("results", [])
    if not results:
        raise ExternalAPIError(f"No map results found for: {query}")

    place = results[0]
    place_id = place.get("place_id")
    location = place.get("geometry", {}).get("location", {})

    return {
        "name": place.get("name"),
        "address": place.get("formatted_address"),
        "lat": location.get("lat"),
        "lng": location.get("lng"),
        "place_id": place_id,
        "maps_url": (
            f"https://www.google.com/maps/place/?q=place_id:{place_id}"
            if place_id
            else None
        ),
        "embed_url": (
            f"https://www.google.com/maps/embed/v1/place?key={MAPS_API_KEY}&q=place_id:{place_id}"
            if place_id
            else None
        ),
    }
