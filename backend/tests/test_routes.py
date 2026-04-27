import pytest
from datetime import datetime, timedelta, timezone
import app.services.weather_service as ws
import app.services.records_service as rs
import app.services.geocoding_service as geo_svc
from app.exceptions import GeocodingError, InvalidDateRangeError, RecordNotFoundError

# ─── Weather Routes ────────────────────────────────────────────────────────────


def test_weather_returns_200(client, monkeypatch, fake_geo):
    monkeypatch.setattr(ws, "geocode", lambda _: fake_geo)
    monkeypatch.setattr(
        ws,
        "fetch_weather",
        lambda *_: {
            "name": "Tunis",
            "main": {
                "temp": 22.5,
                "feels_like": 21,
                "temp_min": 20,
                "temp_max": 24,
                "humidity": 60,
            },
            "weather": [{"description": "clear sky", "icon": "01d"}],
            "wind": {"speed": 5},
            "visibility": 10000,
        },
    )
    r = client.get("/weather?q=Tunis")
    assert r.status_code == 200
    assert r.get_json()["city"] == "Tunis"


def test_weather_returns_400_on_missing_query(client):
    r = client.get("/weather")
    assert r.status_code == 400
    assert "error" in r.get_json()


def test_weather_returns_422_on_bad_location(client, monkeypatch):
    monkeypatch.setattr(
        ws, "geocode", lambda _: (_ for _ in ()).throw(GeocodingError("not found"))
    )
    r = client.get("/weather?q=xyzfake")
    assert r.status_code == 422


def test_forecast_returns_200(client, monkeypatch, fake_geo):
    monkeypatch.setattr(ws, "geocode", lambda _: fake_geo)
    monkeypatch.setattr(
        ws,
        "fetch_forecast",
        lambda *_: {
            "list": [
                {
                    "dt": 1710000000,
                    "main": {"temp": 20, "humidity": 55},
                    "weather": [{"description": "clear", "icon": "01d"}],
                }
            ]
        },
    )
    r = client.get("/forecast?q=Tunis")
    assert r.status_code == 200
    assert "forecast" in r.get_json()


# ─── Records Routes ────────────────────────────────────────────────────────────


def _patch_create(monkeypatch, fake_geo, make_forecast_days):
    # Patch at both levels to ensure no real HTTP calls leak through
    monkeypatch.setattr(rs, "geocode", lambda _: fake_geo)
    monkeypatch.setattr(rs, "get_forecast", lambda _: make_forecast_days())
    monkeypatch.setattr(geo_svc, "geocode", lambda _: fake_geo)


def test_create_record_returns_201(client, monkeypatch, fake_geo, make_forecast_days, valid_range):
    _patch_create(monkeypatch, fake_geo, make_forecast_days)
    start_date, end_date = valid_range
    r = client.post(
        "/records",
        json={
            "location": "Tunis",
            "start_date": start_date,
            "end_date": end_date,
        },
    )
    assert r.status_code == 201
    data = r.get_json()
    assert data["city"] == "Tunis"
    assert "id" in data


def test_create_record_missing_fields(client):
    r = client.post("/records", json={"location": "Tunis"})
    assert r.status_code == 400


def test_create_record_invalid_dates(client):
    r = client.post(
        "/records",
        json={"location": "Tunis", "start_date": "bad-date", "end_date": "2024-06-05"},
    )
    assert r.status_code == 400


def test_get_records_returns_list(client, monkeypatch, fake_geo, make_forecast_days, valid_range):
    _patch_create(monkeypatch, fake_geo, make_forecast_days)
    start_date, end_date = valid_range
    client.post(
        "/records",
        json={
            "location": "Tunis",
            "start_date": start_date,
            "end_date": end_date,
        },
    )
    r = client.get("/records")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)


def test_get_single_record(client, monkeypatch, fake_geo, make_forecast_days, valid_range):
    _patch_create(monkeypatch, fake_geo, make_forecast_days)
    start_date, end_date = valid_range
    created = client.post(
        "/records",
        json={
            "location": "Tunis",
            "start_date": start_date,
            "end_date": end_date,
        },
    ).get_json()
    r = client.get(f"/records/{created['id']}")
    assert r.status_code == 200
    assert r.get_json()["id"] == created["id"]


def test_update_record(client, monkeypatch, fake_geo, make_forecast_days, valid_range):
    _patch_create(monkeypatch, fake_geo, make_forecast_days)
    start_date, end_date = valid_range
    created = client.post(
        "/records",
        json={
            "location": "Tunis",
            "start_date": start_date,
            "end_date": end_date,
        },
    ).get_json()

    new_geo = {"lat": 48.8566, "lon": 2.3522, "city": "Paris", "country": "FR"}
    monkeypatch.setattr(rs, "geocode", lambda _: new_geo)
    monkeypatch.setattr(rs, "get_forecast", lambda _: make_forecast_days())

    r = client.put(f"/records/{created['id']}", json={"location": "Paris"})
    assert r.status_code == 200
    assert r.get_json()["city"] == "Paris"


def test_delete_record(client, monkeypatch, fake_geo, make_forecast_days, valid_range):
    _patch_create(monkeypatch, fake_geo, make_forecast_days)
    start_date, end_date = valid_range
    created = client.post(
        "/records",
        json={
            "location": "Tunis",
            "start_date": start_date,
            "end_date": end_date,
        },
    ).get_json()
    r = client.delete(f"/records/{created['id']}")
    assert r.status_code == 200
    r2 = client.get(f"/records/{created['id']}")
    assert r2.status_code == 404


def test_delete_nonexistent_record(client):
    r = client.delete("/records/9999")
    assert r.status_code == 404


def test_export_json(client, monkeypatch, fake_geo, make_forecast_days, valid_range):
    _patch_create(monkeypatch, fake_geo, make_forecast_days)
    start_date, end_date = valid_range
    client.post(
        "/records",
        json={
            "location": "Tunis",
            "start_date": start_date,
            "end_date": end_date,
        },
    )
    r = client.get("/records/export?format=json")
    assert r.status_code == 200
    assert r.content_type == "application/json"


def test_export_csv(client, monkeypatch, fake_geo, make_forecast_days, valid_range):
    _patch_create(monkeypatch, fake_geo, make_forecast_days)
    start_date, end_date = valid_range
    client.post(
        "/records",
        json={
            "location": "Tunis",
            "start_date": start_date,
            "end_date": end_date,
        },
    )
    r = client.get("/records/export?format=csv")
    assert r.status_code == 200
    assert "text/csv" in r.content_type


def test_export_xml(client, monkeypatch, fake_geo, make_forecast_days, valid_range):
    _patch_create(monkeypatch, fake_geo, make_forecast_days)
    start_date, end_date = valid_range
    client.post(
        "/records",
        json={
            "location": "Tunis",
            "start_date": start_date,
            "end_date": end_date,
        },
    )
    r = client.get("/records/export?format=xml")
    assert r.status_code == 200
    assert "xml" in r.content_type


def test_export_unsupported_format(client):
    r = client.get("/records/export?format=pdf")
    assert r.status_code == 400
