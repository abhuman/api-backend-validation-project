import requests
from config.config import BASE_URL

def test_login_api_valid_credentials():
    response = requests.post(
        f"{BASE_URL}/login",
        json={"username": "test_user", "password": "Test@123"}
    )

    assert response.status_code == 200
    assert "token" in response.json()
