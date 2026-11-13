# Buildlog — Product Scope

**Product:** Buildlog  
**Positioning:** Personal Engineering Intelligence Platform  
**Tagline:** Build. Learn. Measure. Reflect.  
**Status:** V1 product baseline

## 1. Vision

Buildlog brings projects, development activity, learning, experiments, technical decisions, and outcomes into one reliable system.

It provides:
1. A private workspace for managing and reviewing engineering work.
2. A public, curated engineering profile integrated into the user's existing personal portfolio.

Buildlog must distinguish activity from outcomes. Commits, pull requests, and learning sessions are evidence of activity; completed deliverables and verified milestones are evidence of outcomes.

## 2. Initial project registry

The initial registry may include Airlytics, DataGuard / CommerceGuard (canonical name to confirm), Akath Prakashan, Personal Portfolio, AI/RAG experiments, and Data Analytics learning. Names, repository mappings, status, and visibility remain editable. Do not assume every entry is active.

## 3. Product modules

### Project management
Create, edit, archive, and categorize projects; associate repositories; define milestones, weighted deliverables, tasks, priorities, due dates, blockers, architecture, and next actions.

### GitHub integration
Connect GitHub securely, discover accessible repositories, map repositories to projects, and ingest commits, pull requests, issues, and reviews. Support initial backfill, incremental sync, pagination, deduplication, manual refresh, and later webhook ingestion.

Metric integrity:
- A `git pull` is synchronization, not a contribution.
- Deduplicate commits by repository and SHA.
- Separate user-authored activity from total repository activity.
- Do not attribute other contributors' work to the user.
- Expose source and last-sync timestamps.
- Treat Buildlog's heatmap as its own metric, not a replica of GitHub's contribution graph rules.

### Learning management
Create learning tracks and skill categories; record sessions, duration, notes, and resources; link learning to projects and practical exercises. Evidence levels: Explored, Practiced, Applied, Demonstrated. Hours alone do not prove proficiency.

### Engineering timeline
Chronological feed of GitHub events, milestones, releases, learning sessions, project updates, decisions, experiments, and achievements. Preserve event provenance.

### Engineering analytics
Daily, weekly, and monthly activity summaries; project distribution; learning versus building; milestone trends; contribution history; project inactivity; historical snapshots. Avoid a single opaque productivity score.

### Project Observatory
Project objectives, repositories, stack, roadmap, milestones, activity, decisions, challenges, outcomes, and next action.

### Skill Intelligence Map
Connect skills to learning sessions, projects, and demonstrable evidence. Keep skill levels evidence-backed and user-reviewable.

### Experiment Lab
Capture hypothesis, objective, time budget, technologies, findings, limitations, outcome, and next decision: abandon, revisit, or promote.

### Engineering Journal
Technical decision records, weekly reviews, and monthly retrospectives. AI may draft summaries, but the user reviews and approves them.

### AI intelligence (later)
Evidence-grounded summaries, stalled-project detection, learning/project suggestions, and documentation insights. AI must distinguish observed facts from suggestions and never invent progress.

## 4. Private and public experiences

**Private workspace:** all authorized projects, repository metadata permitted by scopes, tasks, notes, learning logs, experiments, decisions, analytics, and sync controls.

**Public profile:** only explicitly published project summaries, case studies, selected milestones, approved GitHub activity, demonstrated skills, and selected timeline entries.

Use dedicated public API response models with allowlisted fields. Never expose private notes, unpublished projects, tokens, employer-confidential information, or raw private repository data.

## 5. Portfolio integration — core requirement

Buildlog is standalone and integrated into the existing personal portfolio:
- Add a route/section such as `/buildlog`, matching the existing router.
- Keep the portfolio's current visual identity, navigation, typography, and design system.
- The private workspace may have its own visual language.
- The portfolio consumes Buildlog's public API; it never connects directly to the database.
- Provide explicit publishing and unpublishing controls.
- Integration must not break existing routes or deployment.

Public sections: Engineering Overview, What I'm Building, Selected Projects, GitHub Activity, Demonstrated Skills, Learning & Exploration, Selected Engineering Timeline, Achievements.

## 6. V1 scope

1. Project registry and milestone management.
2. Secure single-user authentication.
3. GitHub account connection and repository mapping.
4. Initial and incremental ingestion of commits, PRs, and issues.
5. Sync history, retries, pagination, deduplication, checkpoints, and timestamps.
6. PostgreSQL daily analytics and global/per-project heatmaps.
7. Learning tracks and logs.
8. Engineering timeline.
9. Private overview and project pages.
10. Explicit public publishing controls and public API.
11. Portfolio integration.
12. Tests, deployment configuration, and documentation.

## 7. Deferred

Multi-user SaaS, microservices, Kafka, Kubernetes, graph databases, advanced autonomous agents, real-time streaming analytics, complex gamification, and integrations with employer systems are out of scope for the initial release.

## 8. Product principles

Data accuracy before polish; evidence before claims; outcomes separate from activity; private by default; API-first integration; modular monolith first; incremental delivery; portfolio compatibility as a release requirement.
