import pytest

from app.core.config import settings


@pytest.fixture(scope='session')
def celery_config():
    return {
        #     broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        #     backend=str(settings.SYNC_CELERY_DATABASE_URI),
        #     include="app.api.celery_task",  # route where tasks are defined
        'broker_url': f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        'result_backend': str(settings.SYNC_CELERY_DATABASE_URI),
        'include':  "app.api.celery_task" # required for test coverage
    }

pytest_plugins = ("celery.contrib.pytest", )