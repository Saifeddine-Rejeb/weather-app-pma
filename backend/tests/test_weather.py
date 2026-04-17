import app.services.weather_service as weather_service


def test_get_weather_returns_formatted_data(monkeypatch):

    def fake_geocode(location):
        return {
            "lat": 36.8065,
            "lon": 10.1815,
            "city": "Tunis",
            "country": "TN",
        }

    def fake_fetch_weather(lat, lon):
        return {
            "name": "Tunis",
            "main": {"temp": 22.5},
            "weather": [{"description": "clear sky"}],
        }

    monkeypatch.setattr(weather_service, "geocode", fake_geocode)
    monkeypatch.setattr(weather_service, "fetch_weather", fake_fetch_weather)

    result = weather_service.get_weather("Tunis")

    assert result == {
        "city": "Tunis",
        "temperature": 22.5,
        "description": "clear sky",
    }
