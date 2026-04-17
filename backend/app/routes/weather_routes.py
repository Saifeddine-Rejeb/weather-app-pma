from flask import Blueprint, request, jsonify
from app.services.weather_service import get_weather, get_forecast

weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/weather")
def weather():
    location = request.args.get("q")

    if not location:
        return {"error": "q (location) is required"}, 400

    try:
        data = get_weather(location)
        return jsonify(data)
    except Exception:
        return {"error": "failed to fetch weather"}, 500



forecast_bp = Blueprint("forecast", __name__)

@forecast_bp.route("/forecast")
def forecast():
    location = request.args.get("q")

    if not location:
        return {"error": "q (location) is required"}, 400

    try:
        data = get_forecast(location)
        return jsonify(data)
    except Exception:
        return {"error": "failed to fetch forecast"}, 500