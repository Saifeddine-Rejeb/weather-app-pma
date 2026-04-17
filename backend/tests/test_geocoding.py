import app.services.geocoding_service as geocoding_service


def test_geocode_returns_coords_when_input_is_coordinates():
    result = geocoding_service.geocode("36.8065,10.1815")

    assert result["lat"] == 36.8065
    assert result["lon"] == 10.1815
    assert result["city"] is None


def test_geocode_zip_returns_expected_data(monkeypatch):
    class FakeResponse:
        status_code = 200

        def json(self):
            return {
                "lat": 36.8,
                "lon": 10.18,
                "name": "Tunis",
                "country": "TN",
            }

    monkeypatch.setattr(
        geocoding_service.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(),
    )

    result = geocoding_service.geocode_zip("1000")

    assert result == {
        "lat": 36.8,
        "lon": 10.18,
        "city": "Tunis",
        "country": "TN",
    }


def test_geocode_falls_back_to_text_when_zip_fails(monkeypatch):
    monkeypatch.setattr(geocoding_service, "is_coords", lambda _: False)
    monkeypatch.setattr(geocoding_service, "is_zip", lambda _: True)
    monkeypatch.setattr(geocoding_service, "geocode_zip", lambda _: None)

    monkeypatch.setattr(
        geocoding_service,
        "geocode_text",
        lambda _: {
            "lat": 48.8566,
            "lon": 2.3522,
            "city": "Paris",
            "country": "FR",
        },
    )

    result = geocoding_service.geocode("Paris")

    assert result["city"] == "Paris"
