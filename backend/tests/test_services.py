import app.services.weather_service as weather_service


def test_get_weather(monkeypatch):
    monkeypatch.setattr(
        weather_service,
        "fetch_weather",
        lambda city: {
            "name": "Tunis",
            "main": {"temp": 22.5},
            "weather": [{"description": "clear sky"}],
        },
    )

    data = weather_service.get_weather("Tunis")

    assert data["city"] == "Tunis"
    assert data["temperature"] == 22.5
    assert data["description"] == "clear sky"
