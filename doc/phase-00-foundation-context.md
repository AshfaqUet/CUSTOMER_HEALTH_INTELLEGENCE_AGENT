# Phase 00 Foundation Context

## Scope

Phase 00 creates the project foundation for the Customer Health Projection Agent MVP.

The user-selected backend framework is FastAPI. The AGENTS.md guidance remains otherwise unchanged.

## Included

- FastAPI backend skeleton.
- SQLAlchemy session setup.
- Alembic migration scaffolding.
- Pytest backend test setup.
- React, TypeScript, and Vite frontend skeleton.
- Vitest frontend test setup.
- Docker Compose services for PostgreSQL and Redis.
- Environment example files.
- Base documentation placeholders.

## Excluded

- Auth and RBAC implementation.
- Domain models.
- GitHub polling.
- AI provider integration.
- Human review workflow.
- Scoring formulas and score history.
- Dashboard tabs and business logic.
- Post-MVP integrations.

## Architecture Direction

The repository is a monorepo with clearly separated backend and frontend folders. The backend is prepared for future SQLAlchemy models and Alembic migrations without defining MVP domain tables yet. The frontend is prepared for future dashboard implementation without adding dashboard behavior in this phase.
