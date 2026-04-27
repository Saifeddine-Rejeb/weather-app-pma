import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from app.db import db


def create_app():
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    database_url = os.getenv("DATABASE_URL", "sqlite:///weather.db")
    
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.weather_routes import weather_bp
    from app.routes.enrichment_routes import enrichment_bp
    from app.routes.records_routes import records_bp

    app.register_blueprint(weather_bp)
    app.register_blueprint(enrichment_bp)
    app.register_blueprint(records_bp)

    return app