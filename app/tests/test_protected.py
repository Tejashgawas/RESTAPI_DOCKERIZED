def test_protected_route(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/auth/profile", headers=headers)
    print("DEBUG RESPONSE JSON:", response.json)  # 👈 Add this line to see full response
    print("DEBUG STATUS CODE:", response.status_code)

    assert response.status_code == 200
    assert response.json["message"] == "Profile fetched"
    assert response.json["data"]["username"] == "test1"

def test_protected_route_no_token(client):
    response = client.get("/auth/profile")
    assert response.status_code == 401
    assert response.json["message"] == "Access token missing"

def test_protected_route_invalid_token(client):
    headers = {"Authorization": "Bearer invalidtoken123"}
    response = client.get("/auth/profile", headers=headers)
    print("DEBUG RESPONSE JSON:", response.json)
    assert response.status_code == 401
    assert response.json["message"] == "Token is invalid"




