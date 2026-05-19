# Phase 01 RBAC Implementation

## Backend

- Added SQLAlchemy models for `users`, `customers`, `projects`, and `project_ownership`.
- Added Alembic revision `20260519_0001` for the Phase 01 tables and constraints.
- Added Pydantic schemas for users, customers, projects, and ownership.
- Added a simulated current-user dependency using the `X-User-Id` header.
- Added admin-only mutation checks.
- Added role-based read filtering for customers, projects, and project ownership.
- Added project ownership validation:
  - owner user IDs must match the required roles;
  - a project can have only one ownership row;
  - a DL cannot be assigned to more than one active non-completed project.

## API Endpoints

- `GET /auth/current-user`
- `POST /users`
- `GET /users`
- `GET /users/{user_id}`
- `PATCH /users/{user_id}`
- `POST /customers`
- `GET /customers`
- `GET /customers/{customer_id}`
- `PATCH /customers/{customer_id}`
- `POST /projects`
- `GET /projects`
- `GET /projects/{project_id}`
- `PATCH /projects/{project_id}`
- `POST /project-ownership`
- `GET /project-ownership`
- `GET /project-ownership/{ownership_id}`
- `PATCH /project-ownership/{ownership_id}`

## Frontend

- Replaced the Phase 00 landing screen with a basic Admin Configuration shell.
- Added sections for Users, Customers, Projects, and Project Ownership.
- Added a role-aware foundation strip showing Admin action mode and view-only roles.
- The UI is currently static/mock data and does not yet call the API.

## Guardrails

No GitHub ingestion, deliverables, AI analysis, scoring, human review, full dashboard tabs, or post-MVP integrations were implemented.
