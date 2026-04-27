import pytest
from app.services import records_service
from app.exceptions import InvalidDateRangeError, GeocodingError, RecordNotFoundError

FAKE_GEO = {"lat": 36.8, "lon": 10.18, "city": "Tunis", "country": "TN"}
FAKE_WEATHER = {"temperature": 22.5, "description": "clear sky"}


def test_create_record_success(app, monkeypatch):
    monkeypatch.setattr(records_service, "geocode", lambda _: FAKE_GEO)
    monkeypatch.setattr(records_service, "get_weather", lambda _: FAKE_WEATHER)

    with app.app_context():
        record = records_service.create_record("Tunis", "2024-06-01", "2024-06-05")
        assert record.id is not None
        assert record.city == "Tunis"
        assert record.temperature == 22.5


def test_create_record_invalid_date_format(app):
    with app.app_context():
        with pytest.raises(InvalidDateRangeError, match="YYYY-MM-DD"):
            records_service.create_record("Tunis", "01-06-2024", "05-06-2024")


def test_create_record_start_after_end(app, monkeypatch):
    monkeypatch.setattr(records_service, "geocode", lambda _: FAKE_GEO)
    monkeypatch.setattr(records_service, "get_weather", lambda _: FAKE_WEATHER)

    with app.app_context():
        with pytest.raises(InvalidDateRangeError, match="before or equal"):
            records_service.create_record("Tunis", "2024-06-10", "2024-06-01")


def test_create_record_invalid_location(app, monkeypatch):
    monkeypatch.setattr(
        records_service,
        "geocode",
        lambda _: (_ for _ in ()).throw(GeocodingError("not found")),
    )

    with app.app_context():
        with pytest.raises(GeocodingError):
            records_service.create_record("xyzfake", "2024-06-01", "2024-06-05")


def test_get_record_not_found(app):
    with app.app_context():
        with pytest.raises(RecordNotFoundError):
            records_service.get_record_by_id(9999)


def test_update_record_location(app, monkeypatch):
    monkeypatch.setattr(records_service, "geocode", lambda _: FAKE_GEO)
    monkeypatch.setattr(records_service, "get_weather", lambda _: FAKE_WEATHER)

    with app.app_context():
        record = records_service.create_record("Tunis", "2024-06-01", "2024-06-05")
        new_geo = {"lat": 48.8566, "lon": 2.3522, "city": "Paris", "country": "FR"}
        monkeypatch.setattr(records_service, "geocode", lambda _: new_geo)

        updated = records_service.update_record(record.id, {"location": "Paris"})
        assert updated.city == "Paris"


def test_delete_record(app, monkeypatch):
    monkeypatch.setattr(records_service, "geocode", lambda _: FAKE_GEO)
    monkeypatch.setattr(records_service, "get_weather", lambda _: FAKE_WEATHER)

    with app.app_context():
        record = records_service.create_record("Tunis", "2024-06-01", "2024-06-05")
        record_id = record.id
        records_service.delete_record(record_id)

        with pytest.raises(RecordNotFoundError):
            records_service.get_record_by_id(record_id)
