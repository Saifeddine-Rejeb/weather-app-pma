from datetime import datetime, timedelta, timezone

from app.db import db
from app.models.weather_record import WeatherRecord
from app.services.geocoding_service import geocode
from app.services.weather_service import get_forecast
from app.exceptions import RecordNotFoundError, InvalidDateRangeError


def _parse_date(value: str, field_name: str):
    """Parse a YYYY-MM-DD string. Raises InvalidDateRangeError on bad format."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise InvalidDateRangeError(f"'{field_name}' must be in YYYY-MM-DD format.")


def _validate_date_range(start, end):
    if start > end:
        raise InvalidDateRangeError(
            "'start_date' must be before or equal to 'end_date'."
        )


def _validate_forecast_window(start, end):
    today = datetime.now(timezone.utc).date()
    max_end = today + timedelta(days=5)

    if start < today:
        raise InvalidDateRangeError("'start_date' must be today or later.")
    if end > max_end:
        raise InvalidDateRangeError("'end_date' must be within 5 days from today.")


def _extract_temperatures_for_range(forecast_data: dict, start, end) -> list[dict]:
    entries = []
    for day in forecast_data.get("forecast", []):
        day_date = _parse_date(day.get("date"), "forecast.date")
        if start <= day_date <= end:
            entries.append(
                {
                    "date": day["date"],
                    "temp_min": day["temp_min"],
                    "temp_max": day["temp_max"],
                }
            )

    if not entries:
        raise InvalidDateRangeError(
            "No forecast data found for the selected date range. Choose a range between today and the next 5 days."
        )

    return entries


def create_record(location: str, start_date: str, end_date: str) -> WeatherRecord:
    start = _parse_date(start_date, "start_date")
    end = _parse_date(end_date, "end_date")
    _validate_date_range(start, end)
    _validate_forecast_window(start, end)

    # Geocode validates the location exists — raises GeocodingError if not
    geo = geocode(location)
    forecast_data = get_forecast(location)
    range_temperatures = _extract_temperatures_for_range(forecast_data, start, end)
    first_day = range_temperatures[0]

    representative_temp = round(
        (first_day["temp_min"] + first_day["temp_max"]) / 2,
        1,
    )
    first_description = next(
        (
            day.get("description")
            for day in forecast_data.get("forecast", [])
            if day.get("date") == first_day["date"]
        ),
        None,
    )

    record = WeatherRecord(
        location=location,
        city=geo["city"],
        country=geo["country"],
        lat=geo["lat"],
        lon=geo["lon"],
        start_date=start,
        end_date=end,
        temperature=representative_temp,
        description=first_description,
        daily_temperatures=range_temperatures,
    )

    db.session.add(record)
    db.session.commit()
    return record


def get_all_records() -> list[WeatherRecord]:
    return WeatherRecord.query.order_by(WeatherRecord.created_at.desc()).all()


def get_record_by_id(record_id: int) -> WeatherRecord:
    record = db.session.get(WeatherRecord, record_id)
    if not record:
        raise RecordNotFoundError(f"Record {record_id} not found.")
    return record


def update_record(record_id: int, data: dict) -> WeatherRecord:
    record = get_record_by_id(record_id)

    if "location" in data:
        new_location = data["location"].strip()
        if not new_location:
            raise ValueError("'location' cannot be empty.")
        geo = geocode(new_location)
        record.location = new_location
        record.city = geo["city"]
        record.country = geo["country"]
        record.lat = geo["lat"]
        record.lon = geo["lon"]

    # Handle partial date updates — fall back to existing values
    new_start_str = data.get("start_date", record.start_date.isoformat())
    new_end_str = data.get("end_date", record.end_date.isoformat())

    new_start = _parse_date(new_start_str, "start_date")
    new_end = _parse_date(new_end_str, "end_date")
    _validate_date_range(new_start, new_end)
    _validate_forecast_window(new_start, new_end)

    forecast_data = get_forecast(record.location)
    range_temperatures = _extract_temperatures_for_range(forecast_data, new_start, new_end)
    first_day = range_temperatures[0]

    record.temperature = round((first_day["temp_min"] + first_day["temp_max"]) / 2, 1)
    record.description = next(
        (
            day.get("description")
            for day in forecast_data.get("forecast", [])
            if day.get("date") == first_day["date"]
        ),
        record.description,
    )
    record.daily_temperatures = range_temperatures

    record.start_date = new_start
    record.end_date = new_end

    db.session.commit()
    return record


def delete_record(record_id: int) -> None:
    record = get_record_by_id(record_id)
    db.session.delete(record)
    db.session.commit()
