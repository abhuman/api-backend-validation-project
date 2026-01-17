import requests
from config.config import BASE_URL

def test_create_user_missing_email():
    payload = {
        "username": "invalid_user",
        "password": "Test@123"
    }

    response = requests.post(
        f"{BASE_URL}/users",
        json=payload
    )

    assert response.status_code == 400
    assert "email" in response.json()["error"]
