import time

import pytest
from fastapi.testclient import TestClient
from typing import AsyncGenerator

from app.api.v1.endpoints.async_job import TaskResponse
from app.main import app
from app.core.config import settings

url = "http://fastapi.localhost:1080/api/v1"
test_client = TestClient(app, base_url=url)

def test(celery_worker):
    input = 1
    response = TaskResponse(**test_client.post("async_job/increment_task", json={
      "delay": input
    }).json())
    id = response.task_id
    for tries in range(9):
        response = TaskResponse(**test_client.get(f"async_job/increment_task/{id}").json())
        if response.ready:
            assert response.result == input + 1
        else:
            time.sleep(0.5)

