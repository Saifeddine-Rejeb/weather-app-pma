from sqlalchemy import func
from app.db import db


class WeatherRecord(db.Model):
    __tablename__ = "weather_records"

    id = db.Column(db.Integer, primary_key=True)

    # Location
    location = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100))
    country = db.Column(db.String(10))
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    # Date range requested by user
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # Weather snapshot at time of record creation
    temperature = db.Column(db.Float)
    description = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "location": self.location,
            "city": self.city,
            "country": self.country,
            "lat": self.lat,
            "lon": self.lon,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "temperature": self.temperature,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
