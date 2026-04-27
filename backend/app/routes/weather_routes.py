from flask import Blueprint, request, jsonify

from app.services.weather_service import get_weather, get_forecast, get_air_quality
from app.exceptions import GeocodingError, WeatherClientError

weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/weather")
def weather():
    location = request.args.get("q", "").strip()
    if not location:
        return jsonify({"error": "'q' (location) parameter is required."}), 400

    try:
        return jsonify(get_weather(location))
    except GeocodingError as e:
        return jsonify({"error": str(e)}), 422
    except WeatherClientError as e:
        return jsonify({"error": str(e)}), 502
    except Exception:
        return jsonify({"error": "Unexpected error fetching weather."}), 500


@weather_bp.route("/forecast")
def forecast():
    location = request.args.get("q", "").strip()
    if not location:
        return jsonify({"error": "'q' (location) parameter is required."}), 400

    try:
        return jsonify(get_forecast(location))
    except GeocodingError as e:
        return jsonify({"error": str(e)}), 422
    except WeatherClientError as e:
        return jsonify({"error": str(e)}), 502
    except Exception:
        return jsonify({"error": "Unexpected error fetching forecast."}), 500


@weather_bp.route("/air-quality")
def air_quality():
    location = request.args.get("q", "").strip()
    if not location:
        return jsonify({"error": "'q' (location) parameter is required."}), 400

    try:
        return jsonify(get_air_quality(location))
    except GeocodingError as e:
        return jsonify({"error": str(e)}), 422
    except WeatherClientError as e:
        return jsonify({"error": str(e)}), 502
    except Exception:
        return jsonify({"error": "Unexpected error fetching air quality."}), 500
