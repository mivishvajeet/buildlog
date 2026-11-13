# Buildlog API

FastAPI backend for the Buildlog Personal Engineering Intelligence Platform.

## Local setup

1. Copy the environment template: `cp .env.example .env`
2. Start PostgreSQL: `docker compose up --build -d db`
3. Apply migrations: `docker compose run --rm api alembic upgrade head`
4. Start the API: `docker compose up --build api`
5. Open [http://localhost:8000/docs](http://localhost:8000/docs).

## Database migrations

```bash
docker compose run --rm api alembic revision --autogenerate -m "describe schema change"
docker compose run --rm api alembic upgrade head
docker compose run --rm api alembic downgrade -1
```

## Run tests locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

The initial schema includes users, projects, repositories, project-repository mappings, milestones, and tasks. Authentication and owner-scoped CRUD endpoints are deliberately deferred until the authentication design is implemented.
