# HarfangLab Tech Test — Video Game API

A REST API to manage a video game database, built with FastAPI, SQLModel, and PostgreSQL.

## Prerequisites

- [Docker](https://www.docker.com/)
- [uv](https://github.com/astral-sh/uv) for local development

Install uv:
```sh
curl -Ls https://astral.sh/uv/install.sh | sh
```

## Quick Start

```sh
make build-dev
make dev-start
```

The API will be available at http://localhost:8080.  
Interactive docs: http://localhost:8080/docs

## Running Tests

Tests use an in-memory SQLite database and require no running services:

```sh
uv run pytest tests/ -v
```


## API Endpoints

### Video Games

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/video-games/` | List and filter games |
| `POST` | `/video-games/` | Create a game |
| `GET` | `/video-games/{uuid}` | Get a game |
| `PATCH` | `/video-games/{uuid}` | Update a game |
| `DELETE` | `/video-games/{uuid}` | Delete a game |

### Filtering & Pagination

`GET /video-games/` accepts the following query parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Partial name search (case-insensitive) |
| `studio` | string | Partial studio search (case-insensitive) |
| `platform` | string | Exact platform (`PC`, `PS3`, `PS4`, `PS5`, `Switch`, `One`, `WiiU`) |
| `release_date_from` | date | Filter games released from this date |
| `release_date_to` | date | Filter games released up to this date |
| `min_ratings` | int (0–20) | Minimum rating |
| `max_ratings` | int (0–20) | Maximum rating |
| `limit` | int (1–100) | Results per page (default: 20) |
| `offset` | int | Pagination offset (default: 0) |

### Game Schema

```json
{
  "name": "The Witcher 3 : Wild Hunt",
  "release_date": "2015-05-19",
  "studio": "CD Projekt RED",
  "ratings": 19,
  "platform": "PC"
}
```

## Features

- CRUD operations for video games
- Fuzzy duplicate detection — rejects games whose name is too similar to an existing one (threshold: 90/100)
- Input validation — empty names and invalid platforms are rejected
- Pagination and filtering on list endpoint
- Alembic migrations
- Pytest test suite

## Project Structure

```
src/app/
├── main.py               # App entry point
├── config.py             # Settings (pydantic-settings)
├── dependencies.py       # DB session dependency
├── exception_handlers.py # Global exception handlers
└── games/
    ├── models.py         # SQLModel table model
    ├── schemas.py        # Pydantic schemas
    ├── repository.py     # DB queries
    ├── service.py        # Business logic
    ├── router.py         # FastAPI routes
    └── exceptions.py     # Domain exceptions
```
