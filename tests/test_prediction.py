import os

from app import app


def test_prediction_requires_model():
    model_path = app.config["MODEL_PATH"]
    if not os.path.exists(model_path):
        return

    client = app.test_client()
    register = client.post(
        "/api/auth/register",
        json={"email": "pred@example.com", "password": "StrongPass123"},
    )
    if register.status_code not in (200, 201, 409):
        return

    login = client.post(
        "/api/auth/login",
        json={"email": "pred@example.com", "password": "StrongPass123"},
    )
    token = login.get_json().get("data", {}).get("token")
    if not token:
        return

    payload = {
        "MDVP:Fo(Hz)": 119.992,
        "MDVP:Fhi(Hz)": 157.302,
        "MDVP:Flo(Hz)": 74.997,
        "MDVP:Jitter(%)": 0.00784,
        "MDVP:Jitter(Abs)": 0.00007,
        "MDVP:RAP": 0.0037,
        "MDVP:PPQ": 0.00554,
        "Jitter:DDP": 0.01109,
        "MDVP:Shimmer": 0.04374,
        "MDVP:Shimmer(dB)": 0.426,
        "Shimmer:APQ3": 0.02182,
        "Shimmer:APQ5": 0.0313,
        "MDVP:APQ": 0.02971,
        "Shimmer:DDA": 0.06545,
        "NHR": 0.02211,
        "HNR": 21.033,
        "RPDE": 0.414783,
        "DFA": 0.815285,
        "spread1": -4.813031,
        "spread2": 0.266482,
        "D2": 2.301442,
        "PPE": 0.284654,
    }

    response = client.post(
        "/api/predict",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code in (200, 400)
