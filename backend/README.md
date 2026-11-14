# Buildlog API

FastAPI backend for the Buildlog Personal Engineering Intelligence Platform.

## Local setup

1. Copy the environment template: `cp .env.example .env`
2. Start PostgreSQL: `docker compose up --build -d db`
3. Apply migrations: `docker compose run --rm api alembic upgrade head`
4. Start the API: `docker compose up --build api`
5. Open [http://localhost:8001/docs](http://localhost:8001/docs).

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

The initial schema includes users, projects, repositories, project-repository mappings, milestones, and tasks. Authentication provides registration, login, and the current-user endpoint. Project CRUD is available under `/api/v1/projects` and every operation is scoped to the authenticated owner. Milestone and task CRUD will be added in subsequent increments.

## Project API

All project endpoints require `Authorization: Bearer <access_token>`.

- `POST /api/v1/projects` — create a project.
- `GET /api/v1/projects` — list the authenticated user's projects (`offset`, `limit`).
- `GET /api/v1/projects/{project_id}` — retrieve an owned project.
- `PATCH /api/v1/projects/{project_id}` — update an owned project.
- `DELETE /api/v1/projects/{project_id}` — delete an owned project.

Project slugs are generated per user and made unique automatically. Project visibility defaults to private; setting visibility to public does not publish a project. Public publishing is controlled separately by `is_published` and will be exposed through a dedicated publication workflow.
