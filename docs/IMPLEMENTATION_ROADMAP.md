# Buildlog — Implementation Roadmap

**Delivery style:** Incremental, testable releases  
**Target:** V1 private workspace + public portfolio integration  
**Planning note:** Timeline is intentionally milestone-based rather than fixed-date.

## Delivery rules

- Every phase ends with a demonstrable working increment.
- Add tests with each module.
- Update architecture and API documentation when decisions change.
- Never present fixture data as live data.
- Do not build advanced AI before the underlying records and metrics are reliable.
- Preserve the existing portfolio's routes and design system.

## Phase 0 — Repository and project setup

- [ ] Initialize repository and documentation.
- [ ] Add monorepo structure.
- [ ] Add README, product scope, architecture, database design, and roadmap.
- [ ] Add `.gitignore`, `.env.example`, and contribution conventions.
- [ ] Configure basic CI and branch protection.

**Acceptance:** repository initialized, docs committed, no secrets in source control.

## Phase 1 — Backend foundation

- [ ] FastAPI application and versioned router.
- [ ] Configuration and environment handling.
- [ ] PostgreSQL connection.
- [ ] SQLAlchemy models and Alembic.
- [ ] Health endpoint and structured logging.
- [ ] pytest setup.
- [ ] Docker Compose for backend and local PostgreSQL.

**Acceptance:** application starts locally, clean migrations run, health check and tests pass.

## Phase 2 — Project and learning registry

- [ ] User and project models.
- [ ] Project CRUD.
- [ ] Milestone CRUD and weighted progress.
- [ ] Task CRUD.
- [ ] Learning tracks, skills, and learning logs.
- [ ] Validation and ownership checks.

**Acceptance:** projects and learning records can be managed through tested APIs; milestone progress uses weighted outcomes.

## Phase 3 — GitHub connection and ingestion

- [ ] Secure GitHub account connection.
- [ ] Repository discovery and mapping.
- [ ] Commit, pull request, and issue ingestion.
- [ ] Pagination and rate-limit handling.
- [ ] Initial historical backfill.
- [ ] Incremental sync checkpoints.
- [ ] Idempotent upserts and duplicate protection.
- [ ] Sync run history and manual refresh.
- [ ] User identity matching for personal contributions.

**Acceptance:** repeated syncs do not duplicate records; failures are visible and retryable; user activity is distinct from repository-wide activity; tokens are never exposed.

## Phase 4 — Analytics and timeline

- [ ] Daily user and project aggregation.
- [ ] Global account contribution calendar where supported.
- [ ] Repository-specific activity heatmaps.
- [ ] Project activity endpoints.
- [ ] Weekly/monthly trends.
- [ ] Engineering timeline combining GitHub and manual events.
- [ ] Project snapshots.

**Acceptance:** aggregates reconcile with source records; date boundaries respect user timezone; source and last-sync context are visible.

## Phase 5 — Private dashboard

- [ ] React + TypeScript application.
- [ ] Authentication and protected routes.
- [ ] Overview screen.
- [ ] Projects list and detail pages.
- [ ] Activity and heatmap screen.
- [ ] Learning screen.
- [ ] Timeline and weekly review.
- [ ] Settings and sync controls.
- [ ] Responsive and accessible UI.

**Acceptance:** dashboard uses real API data and implements loading, empty, error, and stale-data states.

## Phase 6 — Public profile and portfolio integration

- [ ] Public profile settings.
- [ ] Field-level publication allowlists.
- [ ] Public API response models.
- [ ] Public project and selected activity endpoints.
- [ ] Inspect existing portfolio routing and design tokens.
- [ ] Add Buildlog route/section to existing portfolio.
- [ ] Integration tests and caching.

**Acceptance:** only explicitly published information is public; unpublishing removes content; private notes and repository details remain hidden; existing portfolio pages and deployment are unchanged.

## Phase 7 — Hardening and deployment

- [ ] Production configuration and secret management.
- [ ] Database backups and restore procedure.
- [ ] Error handling and observability.
- [ ] API rate limiting.
- [ ] Dependency and security checks.
- [ ] Deployment and rollback notes.
- [ ] End-to-end smoke tests.

**Acceptance:** production deployment is reproducible, backups are documented, sync failures are observable, access tests pass.

## Phase 8 — Advanced intelligence (post-V1)

- Project Observatory and inactivity alerts.
- Skill Intelligence Map with evidence links.
- Experiment Lab.
- Technical Decision Journal enhancements.
- Grounded AI weekly summaries.
- Monthly Engineering Yearbook.
- Career Evidence Bank.
- Webhook-driven near-real-time ingestion.

Only start after reliable source data and metric definitions exist.

## Suggested V1 release gate

V1 is ready only when:
1. Project and learning records can be managed.
2. GitHub ingestion is repeatable, incremental, and deduplicated.
3. Analytics derive from persisted source data.
4. The private dashboard is functional.
5. The public API exposes only approved data.
6. Buildlog is integrated into the existing portfolio without regressions.
7. Tests, deployment, and operational documentation are in place.
