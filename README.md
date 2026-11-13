# Buildlog

**Personal Engineering Intelligence Platform**  
*Build. Learn. Measure. Reflect.*

Buildlog is a personal command centre for managing engineering projects, tracking development activity, recording learning, and turning verified work into a clear engineering story.

It has two connected experiences:

- **Private workspace:** projects, milestones, tasks, GitHub activity, learning logs, experiments, decisions, analytics, and retrospectives.
- **Public engineering profile:** explicitly approved projects, achievements, selected activity, and demonstrated skills, integrated into the existing personal portfolio.

## Product principles

1. Evidence before claims.
2. Outcomes are separate from activity.
3. Private by default; public only by explicit approval.
4. Data accuracy before visual polish.
5. API-first portfolio integration.
6. Start with a modular monolith; add distributed systems only when justified.

## Planned stack

| Area | Technology |
|---|---|
| Backend | Python, FastAPI, Pydantic |
| Database | PostgreSQL |
| ORM / migrations | SQLAlchemy 2.x / Alembic |
| Frontend | React, TypeScript |
| Styling / charts | Tailwind CSS / Recharts |
| GitHub integration | GitHub REST API, selective GraphQL |
| Jobs | APScheduler initially |
| Runtime | Docker |
| Tests | pytest, HTTPX, frontend test runner |

## Core modules

- Project registry, milestones, and tasks
- GitHub repository mapping and activity ingestion
- Contribution history and repository heatmaps
- Learning tracks, skills, and evidence
- Engineering timeline and weekly reviews
- Project Observatory and Experiment Lab
- Public profile API for portfolio integration

## Documentation

- [Product scope](BUILDLOG_PRODUCT_SCOPE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Database design](docs/DATABASE_DESIGN.md)
- [Implementation roadmap](docs/IMPLEMENTATION_ROADMAP.md)

## V1 delivery sequence

1. Backend and database foundation
2. Project and learning registry
3. GitHub connection and idempotent ingestion
4. Analytics and engineering timeline
5. Private dashboard
6. Public publishing API and portfolio integration
7. Security, tests, deployment, and operational hardening

## Important metric rules

- A `git pull` is synchronization, not a contribution.
- A commit is counted once, using repository identity and commit SHA.
- Personal contributions are distinct from total repository activity.
- Project progress is based on weighted milestone completion, not commit volume.
- Imported metrics show their source and last-sync timestamp.

## Privacy

The private workspace is authenticated. The public API returns only allowlisted, explicitly published fields. Never expose access tokens, private notes, unpublished projects, or private repository details.

## Status

Product definition and architecture baseline are documented. Implementation has not yet started.
