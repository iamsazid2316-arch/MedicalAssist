def test_cadet_login_returns_token_and_role(client):
    response = client.post(
        "/login", data={"username": "TestCadet", "password": "test123"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["name"] == "TestCadet"
    assert data["role"] == "cadet"


def test_doctor_login_returns_token_and_role(client):
    response = client.post(
        "/login", data={"username": "TestDoctor", "password": "doctor123"}
    )

    assert response.status_code == 200
    assert response.json()["role"] == "doctor"


def test_wrong_password_is_rejected(client):
    response = client.post(
        "/login", data={"username": "TestCadet", "password": "wrongpassword"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid name or password"


def test_protected_route_requires_token(client):
    response = client.get("/cases")

    assert response.status_code == 401
