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
# renovate: datasource=pypi depName=poetry versioning=pep440
ENV POETRY_VERSION="2.1.4"
RUN pip install poetry=="${POETRY_VERSION}" && \
     poetry config virtualenvs.create false

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

# renovate: datasource=repology depName=alpine_3_21/gcc versioning=loose
ENV GCC_VERSION="14.2.0-r4"
# renovate: datasource=repology depName=alpine_3_21/musl-dev versioning=loose
ENV MUSL_DEV_VERSION="1.2.5-r9"
# renovate: datasource=repology depName=alpine_3_21/linux-headers versioning=loose
ENV LINUX_HEADERS_VERSION="6.6-r1"

# Install dependencies needed for testing
RUN apk add --no-cache  \
    gcc="${GCC_VERSION}" \
    musl-dev="${MUSL_DEV_VERSION}" \
    linux-headers="${LINUX_HEADERS_VERSION}"

# Install all dependencies including dev dependencies
RUN poetry install --no-root

COPY app/test /opt/app/test

# Switch back to non-root user for running tests
USER appuser
