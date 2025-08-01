import pytest
from fastapi.testclient import TestClient
from src.api.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def test_user():
    # Test user info for registration/login
    return {
        "username": "testuser@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }

@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    # Register the user (if not already registered)
    client.post("/users/register", json=test_user)
    # Log in and get access token
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"],
    }
    response = client.post(
        "/users/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
