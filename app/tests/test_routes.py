# tests/test_routes.py

def test_ping(client):
    response = client.get("/api/ping")
    assert response.status_code == 200
    assert response.json["message"] == "pong"
