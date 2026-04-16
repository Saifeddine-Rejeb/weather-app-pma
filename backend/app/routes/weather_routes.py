from flask import Blueprint, request, jsonify
from app.services.weather_service import get_weather

weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/weather")
def weather():
    city = request.args.get("city")

    if not city or not city.strip():
        return jsonify({"error": "City parameter is required"}), 400

    try:
        data = get_weather(city)
        return jsonify(data), 200
    except KeyError as e:
        return jsonify({"error": f"Missing field in API response: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
