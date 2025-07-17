def test_logout(client, tokens):
    print("Access token:", tokens["access"])
    print("Refresh token:", tokens["refresh"])
    print(client.set_cookie.__code__.co_varnames)


    client.set_cookie("access_token", tokens["access"])
    client.set_cookie("refresh_token", tokens["refresh"])


    response = client.post("/auth/logout")
    print("Logout response JSON:", response.json)

    assert response.status_code == 200
    assert response.json["message"] == "Logged out successfully"
