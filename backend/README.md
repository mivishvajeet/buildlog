# Buildlog API

FastAPI backend for the Buildlog Personal Engineering Intelligence Platform.

## Local setup

1. Copy the environment template:

   ```bash
   cp .env.example .env
   ```

2. Start PostgreSQL and the API:

   ```bash
   docker compose up --build
   ```

3. Open the API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

4. Check the health endpoint:

   ```bash
   curl http://localhost:8000/api/v1/health
   ```

## Run tests locally

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Database models, migrations, authentication, and domain APIs will be added incrementally.
