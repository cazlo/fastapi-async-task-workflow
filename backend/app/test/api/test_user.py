import pytest
from fastapi.testclient import TestClient
from app.main import app
from typing import AsyncGenerator
from app.core.config import settings

url = "http://fastapi.localhost:1080/api/v1"
test_client = TestClient(app, base_url=url)

class TestPostLogin:
    @pytest.mark.parametrize(
        "method, endpoint, data, expected_status, expected_response",
        [
            ("get", "/user", None, 200, None),
            ("get", "/user/list", None, 200, None),
            ("get", "/user/list/by_role_name?user_status=active&page=1&size=50", None, 200, None),            
        ],
    )
    def test(self, method, endpoint, data, expected_status, expected_response):
            credentials = {"email": settings.FIRST_SUPERUSER_EMAIL, "password": settings.FIRST_SUPERUSER_PASSWORD}
            response = test_client.post("/auth/login", json=credentials)
            print(response.json)
            access_token = response.json()["data"]["access_token"]
            if method == "get":
                response = test_client.get(endpoint, headers={"Authorization": f"Bearer {access_token}"})
            elif method == "put":
                response = test_client.put(endpoint, json=data, headers={"Authorization": f"Bearer {access_token}"})
            elif method == "delete":
                response = test_client.delete(endpoint, headers={"Authorization": f"Bearer {access_token}"})
            else:  # Default to POST
                response = test_client.post(endpoint, json=data, headers={"Authorization": f"Bearer {access_token}"})

            assert response.status_code == expected_status
            if expected_response is not None:                
                assert response.json() == expected_response
