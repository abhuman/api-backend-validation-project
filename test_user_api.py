import requests
from config.config import BASE_URL

def test_create_user_api():
    payload = {
        "username": "new_user",
        "email": "new_user@example.com",
        "password": "Test@123"
    }

    response = requests.post(
        f"{BASE_URL}/users",
        json=payload
    )

    assert response.status_code == 201
    assert response.json()["username"] == payload["username"]
