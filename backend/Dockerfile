FROM docker.io/python:3.12-alpine3.21 AS runtime
ENV PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=100
WORKDIR /code
# Install Poetry
RUN apk update
RUN pip install poetry && poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY app/pyproject.toml app/poetry.lock* /code/
# todo non-root user
RUN poetry install --no-root --only main

ENV PYTHONPATH=/code
EXPOSE 8000
# todo code should be on here

FROM runtime AS test
# needed for celery pytest
RUN apk add --no-cache gcc musl-dev linux-headers

RUN poetry install --no-root
