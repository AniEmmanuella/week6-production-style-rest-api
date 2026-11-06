# Architecture

## Overview

The project is a small layered REST API for managing tasks. HTTP requests enter through FastAPI routes, request bodies and query parameters are validated by Pydantic, and SQLAlchemy handles persistence.

## Request flow

1. A client sends an HTTP request to an endpoint.
2. FastAPI matches the route and validates input using the Pydantic schema.
3. Protected task routes invoke the Bearer-token dependency.
4. The route receives a SQLAlchemy database session.
5. The route reads or changes a `Task` ORM model.
6. SQLAlchemy persists changes to SQLite.
7. FastAPI serializes the response using the response schema.

## Main components

- `app/main.py`: application creation, lifespan, routers and database error handler.
- `app/core/config.py`: environment-based application settings.
- `app/core/security.py`: simple Bearer-token authentication dependency.
- `app/db/`: SQLAlchemy declarative base and session dependency.
- `app/models/`: database table definitions.
- `app/schemas/`: Pydantic request and response contracts.
- `app/api/routes/`: HTTP endpoints.
- `tests/`: automated API tests using an isolated in-memory SQLite database.

## Data model

`tasks` contains:
- `id`: integer primary key.
- `title`: required task title.
- `description`: optional longer description.
- `status`: `pending`, `in_progress`, or `completed`.
- `priority`: `low`, `medium`, or `high`.
- `created_at` and `updated_at`: timestamps.

## Security note

The project uses a shared API token to demonstrate authentication concepts. It is not a complete production identity system. A production deployment should use user accounts, password hashing, short-lived signed access tokens, refresh-token rotation, authorization rules, HTTPS, secret management and rate limiting. Change the development token before deployment.

## Database note

SQLite is selected to make local setup simple. For a multi-user production deployment, use a managed PostgreSQL database and configure `DATABASE_URL` accordingly. Add Alembic migrations before evolving production schemas.
