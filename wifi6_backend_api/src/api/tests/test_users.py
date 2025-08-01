def test_register_and_login(client, test_user):
    # Register new user
    resp = client.post("/users/register", json=test_user)
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == test_user["username"]
    assert data["full_name"] == test_user["full_name"]
    assert data["disabled"] is False

    # Registering again should fail (already exists)
    resp2 = client.post("/users/register", json=test_user)
    assert resp2.status_code == 400

    # Login with correct credentials
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"],
    }
    resp3 = client.post(
        "/users/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp3.status_code == 200
    token_data = resp3.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    client.post("/users/register", json=test_user)
    wrong_data = {
        "username": test_user["username"],
        "password": "wrongpassword",
    }
    resp = client.post(
        "/users/login",
        data=wrong_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 400

def test_read_users_me_authenticated(client, auth_headers, test_user):
    resp = client.get("/users/me", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == test_user["username"]

def test_read_users_me_unauthenticated(client):
    resp = client.get("/users/me")
    assert resp.status_code == 401
