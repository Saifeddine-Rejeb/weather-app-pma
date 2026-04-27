from pathlib import Path
import sys
from datetime import datetime, timedelta, timezone
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.db import db as _db


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def fake_geo():
    return {"lat": 36.8, "lon": 10.18, "city": "Tunis", "country": "TN"}


@pytest.fixture
def valid_range():
    today = datetime.now(timezone.utc).date()
    return today.isoformat(), (today + timedelta(days=2)).isoformat()


@pytest.fixture
def make_forecast_days():
    def _build(days: int = 6, city: str = "Tunis", country: str = "TN"):
        today = datetime.now(timezone.utc).date()
        forecast = []
        for i in range(days):
            day = today + timedelta(days=i)
            forecast.append(
                {
                    "date": day.isoformat(),
                    "temp_min": 20.0 + i,
                    "temp_max": 25.0 + i,
                    "description": "clear sky",
                }
            )
        return {"city": city, "country": country, "forecast": forecast}

    return _build
