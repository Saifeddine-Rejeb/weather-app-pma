import pytest
from datetime import datetime, timedelta, timezone
from app.services import records_service
from app.exceptions import InvalidDateRangeError, GeocodingError, RecordNotFoundError

def test_create_record_success(app, monkeypatch, fake_geo, make_forecast_days, valid_range):
    monkeypatch.setattr(records_service, "geocode", lambda _: fake_geo)
    monkeypatch.setattr(records_service, "get_forecast", lambda _: make_forecast_days())
    start_date, end_date = valid_range

    with app.app_context():
        record = records_service.create_record("Tunis", start_date, end_date)
        assert record.id is not None
        assert record.city == "Tunis"
        assert len(record.daily_temperatures) == 3


def test_create_record_invalid_date_format(app):
    with app.app_context():
        with pytest.raises(InvalidDateRangeError, match="YYYY-MM-DD"):
            records_service.create_record("Tunis", "01-06-2024", "05-06-2024")


def test_create_record_start_after_end(app, monkeypatch, fake_geo, make_forecast_days):
    monkeypatch.setattr(records_service, "geocode", lambda _: fake_geo)
    monkeypatch.setattr(records_service, "get_forecast", lambda _: make_forecast_days())

    with app.app_context():
        with pytest.raises(InvalidDateRangeError, match="before or equal"):
            records_service.create_record("Tunis", "2024-06-10", "2024-06-01")


def test_create_record_invalid_location(app, monkeypatch, valid_range):
    monkeypatch.setattr(
        records_service,
        "geocode",
        lambda _: (_ for _ in ()).throw(GeocodingError("not found")),
    )

    with app.app_context():
        with pytest.raises(GeocodingError):
            start_date, end_date = valid_range
            records_service.create_record("xyzfake", start_date, end_date)


def test_create_record_end_date_too_far(app, monkeypatch, fake_geo, make_forecast_days):
    monkeypatch.setattr(records_service, "geocode", lambda _: fake_geo)
    monkeypatch.setattr(records_service, "get_forecast", lambda _: make_forecast_days())

    with app.app_context():
        today = datetime.now(timezone.utc).date()
        with pytest.raises(InvalidDateRangeError, match="within 5 days"):
            records_service.create_record(
                "Tunis",
                today.isoformat(),
                (today + timedelta(days=6)).isoformat(),
            )


def test_get_record_not_found(app):
    with app.app_context():
        with pytest.raises(RecordNotFoundError):
            records_service.get_record_by_id(9999)


def test_update_record_location(app, monkeypatch, fake_geo, make_forecast_days, valid_range):
    monkeypatch.setattr(records_service, "geocode", lambda _: fake_geo)
    monkeypatch.setattr(records_service, "get_forecast", lambda _: make_forecast_days())
    start_date, end_date = valid_range

    with app.app_context():
        record = records_service.create_record("Tunis", start_date, end_date)
        new_geo = {"lat": 48.8566, "lon": 2.3522, "city": "Paris", "country": "FR"}
        monkeypatch.setattr(records_service, "geocode", lambda _: new_geo)
        monkeypatch.setattr(records_service, "get_forecast", lambda _: make_forecast_days())

        updated = records_service.update_record(record.id, {"location": "Paris"})
        assert updated.city == "Paris"


def test_delete_record(app, monkeypatch, fake_geo, make_forecast_days, valid_range):
    monkeypatch.setattr(records_service, "geocode", lambda _: fake_geo)
    monkeypatch.setattr(records_service, "get_forecast", lambda _: make_forecast_days())
    start_date, end_date = valid_range

    with app.app_context():
        record = records_service.create_record("Tunis", start_date, end_date)
        record_id = record.id
        records_service.delete_record(record_id)

        with pytest.raises(RecordNotFoundError):
            records_service.get_record_by_id(record_id)
