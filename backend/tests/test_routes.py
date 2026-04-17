import app.services.weather_service as weather_service


def test_weather_route_returns_200_with_valid_query(client, monkeypatch):
    monkeypatch.setattr(
        weather_service,
        "geocode",
        lambda _: {"lat": 51.5072, "lon": -0.1276, "city": "London", "country": "GB"},
    )

    monkeypatch.setattr(
        weather_service,
        "fetch_weather",
        lambda *_: {
            "name": "London",
            "main": {"temp": 15.0},
            "weather": [{"description": "cloudy"}],
        },
    )

    response = client.get("/weather?q=London")

    assert response.status_code == 200
    assert response.get_json()["city"] == "London"


def test_weather_route_returns_400_when_missing_query(client):
    response = client.get("/weather")

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_weather_route_returns_500_on_service_failure(client, monkeypatch):
    def fail(*args, **kwargs):
        raise Exception("boom")

    monkeypatch.setattr(weather_service, "geocode", fail)

    response = client.get("/weather?q=London")

    assert response.status_code == 500
    assert response.get_json()["error"] == "failed to fetch weather"
