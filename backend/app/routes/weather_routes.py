from flask import Blueprint, request, jsonify
from app.services.weather_service import get_weather

weather_bp = Blueprint("weather", __name__)

@weather_bp.route("/weather")

def weather():
    city = request.args.get("city")
    data = get_weather(city)
    return jsonify(data)