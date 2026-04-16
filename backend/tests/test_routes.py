import app.services.weather_service as weather_service


def test_weather_route_success(client, monkeypatch):
    monkeypatch.setattr(
        weather_service,
        "fetch_weather",
        lambda city: {
            "name": "London",
            "main": {"temp": 15.0},
            "weather": [{"description": "cloudy"}],
        },
    )

    response = client.get("/weather?city=London")

    assert response.status_code == 200
    data = response.get_json()
    assert data["city"] == "London"
    assert data["temperature"] == 15.0


def test_weather_route_missing_city(client):
    response = client.get("/weather")

    assert response.status_code == 400
    assert "error" in response.get_json()
