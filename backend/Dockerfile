FROM docker.io/python:3.13-alpine3.21 AS runtime
ENV PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=100

# Create non-root user and group
RUN addgroup -g 1000 -S appgroup && adduser -u 1000 -S appuser -G appgroup

# Create app directory and set permissions
RUN mkdir -p /opt/app && chown -R appuser:appgroup /opt/app

# Set working directory
WORKDIR /opt/app

# Install Poetry
RUN apk update
RUN pip install poetry && poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY app/pyproject.toml app/poetry.lock* /opt/app/
RUN chown -R appuser:appgroup /opt/app

# Install dependencies
RUN poetry install --no-root --only main

# Copy application code
COPY app/alembic.ini app/poetry.lock app/pyproject.toml /opt/app/
COPY app/alembic /opt/app
COPY app/app /opt/app/app
RUN chown -R appuser:appgroup /opt/app

RUN poetry install --only main

#ENV PYTHONPATH=/opt/app
EXPOSE 8000

# Switch to non-root user
USER appuser

FROM runtime AS test
USER root

# Install dependencies needed for testing
RUN apk add --no-cache gcc musl-dev linux-headers

# Install all dependencies including dev dependencies
RUN poetry install --no-root

COPY app/test /opt/app/test

# Switch back to non-root user for running tests
USER appuser
