from flask import Blueprint, request, jsonify
from .services import get_weather

main = Blueprint("main", __name__)

@main.route("/weather")
def weather():
    city = request.args.get("city")
    data = get_weather(city)
    return jsonify(data)