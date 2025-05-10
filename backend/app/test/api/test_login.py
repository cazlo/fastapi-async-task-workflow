import pytest
from fastapi.testclient import TestClient
from typing import AsyncGenerator
from app.main import app
from app.core.config import settings

url = "http://fastapi.localhost:1080/api/v1"
test_client = TestClient(app, base_url=url)

class TestPostLogin:
    @pytest.mark.parametrize(
        "method, endpoint, data, expected_status, expected_response",
        [
            ("post", "/login", {"email": "incorrect_email@gmail.com", "password": "123456"}, 400, {"detail": "Email or Password incorrect"}),
            ("post", "/login", {"email": settings.FIRST_SUPERUSER_EMAIL, "password": settings.FIRST_SUPERUSER_PASSWORD}, 200, None),
            ("post", "/login", {"email": settings.FIRST_SUPERUSER_EMAIL, "password": "foobar"}, 400, None),
            ("post", "/login/new_access_token", {"refresh_token": ""}, 403, {"detail": "Error when decoding the token. Please check your request."})
        ],
    )
    def test(self, method, endpoint, data, expected_status, expected_response):
            if method == "get":
                response = test_client.get(endpoint)
            elif method == "put":
                response = test_client.put(endpoint, json=data)
            elif method == "delete":
                response = test_client.delete(endpoint)
            else:  # Default to POST
                response = test_client.post(endpoint, json=data)

            assert response.status_code == expected_status
            if expected_response is not None:                
                assert response.json() == expected_response
