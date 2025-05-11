import pytest
from fastapi.testclient import TestClient
from typing import AsyncGenerator
from app.main import app
from app.core.config import settings
from app.schemas.token_schema import Token

url = "http://fastapi.localhost:1080/api/v1"
test_client = TestClient(app, base_url=url)

class TestPostLogin:
    @pytest.mark.parametrize(
        "method, endpoint, data, expected_status, expected_response",
        [
            ("post", "/auth/login", {"email": "incorrect_email@gmail.com", "password": "123456"}, 401, {"detail": "Email or Password incorrect"}),
            ("post", "/auth/login", {"email": settings.FIRST_SUPERUSER_EMAIL, "password": settings.FIRST_SUPERUSER_PASSWORD}, 200, None),
            ("post", "/auth/login", {"email": settings.FIRST_SUPERUSER_EMAIL, "password": "foobar"}, 401, None),
            ("post", "/auth/login", {"email": "user@example.com", "password": settings.FIRST_SUPERUSER_PASSWORD}, 403, None),
            ("post", "/auth/new_access_token", {"refresh_token": ""}, 403, {"detail": "Error when decoding the token. Please check your request."})
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

    def test_login_logout(self):
        user_list_response = test_client.get("/user/list", headers={"Authorization": f"Bearer none"})
        assert user_list_response.status_code == 403

        response = test_client.post("/auth/access-token", data={"username": settings.FIRST_SUPERUSER_EMAIL, "password": settings.FIRST_SUPERUSER_PASSWORD})
        assert response.status_code == 200
        access_token = response.json()['access_token']

        user_list_response = test_client.get("/user/list", headers={"Authorization": f"Bearer {access_token}"})
        assert user_list_response.status_code == 200

        response = test_client.post("/auth/logout", json={}, headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200

        new_user_list_response = test_client.get("/user/list", headers={"Authorization": f"Bearer {access_token}"})
        assert new_user_list_response.status_code == 403