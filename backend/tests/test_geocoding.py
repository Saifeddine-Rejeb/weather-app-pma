import pytest
import app.services.geocoding_service as geo_svc
from app.exceptions import GeocodingError


def test_is_coords_valid():
    assert geo_svc.is_coords("36.8065,10.1815") is True
    assert geo_svc.is_coords(" 48.8566 , 2.3522 ") is True


def test_is_coords_invalid():
    assert geo_svc.is_coords("London") is False
    assert geo_svc.is_coords("1000") is False
    assert geo_svc.is_coords("") is False


def test_parse_coords():
    result = geo_svc.parse_coords("36.8065,10.1815")
    assert result["lat"] == 36.8065
    assert result["lon"] == 10.1815
    assert result["city"] is None


def test_geocode_returns_coords_directly():
    result = geo_svc.geocode("36.8065,10.1815")
    assert result["lat"] == 36.8065
    assert result["lon"] == 10.1815


def test_geocode_zip_success(monkeypatch):
    class FakeResponse:
        status_code = 200

        def json(self):
            return {"lat": 36.8, "lon": 10.18, "name": "Tunis", "country": "TN"}

    monkeypatch.setattr(geo_svc.requests, "get", lambda *a, **kw: FakeResponse())
    result = geo_svc.geocode_zip("1000")
    assert result == {"lat": 36.8, "lon": 10.18, "city": "Tunis", "country": "TN"}


def test_geocode_zip_returns_none_on_404(monkeypatch):
    class FakeResponse:
        status_code = 404

        def json(self):
            return {}

    monkeypatch.setattr(geo_svc.requests, "get", lambda *a, **kw: FakeResponse())
    assert geo_svc.geocode_zip("99999") is None


def test_geocode_text_success(monkeypatch):
    class FakeResponse:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return [{"lat": 48.8566, "lon": 2.3522, "name": "Paris", "country": "FR"}]

    monkeypatch.setattr(geo_svc.requests, "get", lambda *a, **kw: FakeResponse())
    result = geo_svc.geocode_text("Paris")
    assert result["city"] == "Paris"
    assert result["country"] == "FR"


def test_geocode_text_raises_when_empty(monkeypatch):
    class FakeResponse:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return []

    monkeypatch.setattr(geo_svc.requests, "get", lambda *a, **kw: FakeResponse())
    with pytest.raises(GeocodingError, match="not found"):
        geo_svc.geocode_text("xyznonexistent")


def test_geocode_falls_back_from_zip_to_text(monkeypatch):
    monkeypatch.setattr(geo_svc, "is_coords", lambda _: False)
    monkeypatch.setattr(geo_svc, "is_zip", lambda _: True)
    monkeypatch.setattr(geo_svc, "geocode_zip", lambda _: None)
    monkeypatch.setattr(
        geo_svc,
        "geocode_text",
        lambda _: {"lat": 48.8566, "lon": 2.3522, "city": "Paris", "country": "FR"},
    )
    result = geo_svc.geocode("Paris")
    assert result["city"] == "Paris"


def test_geocode_raises_on_empty_string():
    with pytest.raises(GeocodingError, match="empty"):
        geo_svc.geocode("   ")
