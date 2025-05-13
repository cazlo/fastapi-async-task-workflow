# Project Changelog

## v0.2.0  (2025-05)

- Fixing code rot issues (getting code compiling and all tests passing again)
- Version locking more dependencies to avoid future code rot issues
- Multi-stage docker build for test and runtime consistency
- Single docker-compose with multiple runtime profiles
- Pytest coverage reporting
- Python 3.12

## v0.1.17 (2023-04-01)

#### 💅 Polish

- `Migrate from traefik to Caddy as reverse proxy server`

## v0.1.16 (2023-03-25)

#### 💅 Polish

- `Reduce fastapi container size using slim image`
- `Add celery and celery beats example with async schedule feature`

## v0.1.15 (2023-03-23)

#### 💅 Polish

- `Add cleanup and relese memory of ml models when the server shutdown`
- `Add a global context middleware to shere a ml models on handlers`

## v0.1.14 (2023-03-22)

#### 💅 Polish

- `Add sample endpoints to use NLP transformers modles `