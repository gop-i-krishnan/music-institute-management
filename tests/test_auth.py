from fastapi.testclient import TestClient

from app.main import app


# Create test client that simulates real HTTP requests.
client = TestClient(app)


# Verify that login rejects invalid credentials correctly.
def test_invalid_login():

    response = client.post(
        "/login",
        data={
            "username": "wrong@test.com",
            "password": "wrongpassword"
        }
    )

    # Ensure backend returns HTTP 401 Unauthorized.
    assert response.status_code == 401

    # Convert JSON response into Python dictionary.
    data = response.json()

    # Verify standardized error response structure.
    assert data["success"] is False

    assert (
        data["message"]
        == "Invalid email or password"
    )
    
# Verify successful login returns JWT token.
def test_successful_login():

    response = client.post(
        "/login",
        data={
            "username": "admin@test.com",
            "password": "strongpassword"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

    assert data["token_type"] == "bearer"