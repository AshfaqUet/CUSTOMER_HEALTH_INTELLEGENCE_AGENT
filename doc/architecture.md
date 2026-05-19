# Architecture

The repository is organized as a monorepo with separate backend and frontend applications.

- Backend: FastAPI, SQLAlchemy, Alembic, Celery, Redis, PostgreSQL, pytest.
- Frontend: React, TypeScript, Vite, Vitest.
- Local infrastructure: Docker Compose for PostgreSQL and Redis.

## Backend Structure

The backend uses a small layered structure:

- `app/api/routes/` for FastAPI route modules.
- `app/api/deps.py` for request dependencies such as the temporary current-user resolver.
- `app/models/` for SQLAlchemy models.
- `app/schemas/` for Pydantic API contracts.
- `app/services/` for reusable domain rules such as RBAC filtering and project ownership validation.
- `app/db/` for SQLAlchemy base/session setup.
- `alembic/` for migration scripts.

## Phase 01 Domain Foundation

Phase 01 adds:

- users;
- customers;
- projects;
- project ownership.

Project visibility is enforced in backend query logic. Admin sees all projects; VP, Project Director, PM, and DL see only projects where they are assigned in `project_ownership`.

## Frontend Structure

The frontend currently has a minimal Vite app with a basic Admin Configuration shell. It is static in Phase 01 and prepared for future API integration.

## Not Yet Implemented

- Real auth/session infrastructure.
- GitHub ingestion.
- Deliverables.
- AI analysis.
- Scoring engine and score history.
- Full dashboard tabs.
