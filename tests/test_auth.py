from app import app


def test_register_and_login():
    client = app.test_client()

    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "StrongPass123"},
    )
    assert response.status_code in (200, 201, 409)

    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "StrongPass123"},
    )
    assert response.status_code == 200
    assert "token" in response.get_json().get("data", {})
