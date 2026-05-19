# Phase 01 RBAC Validation

## Implemented Scope

- FastAPI Phase 01 identity and RBAC foundation.
- SQLAlchemy models and Alembic migration for users, customers, projects, and project ownership.
- Minimal admin CRUD-style API endpoints.
- Simulated `X-User-Id` current-user dependency for testable permissions.
- Backend RBAC filtering for project/customer/ownership reads.
- DL one-active-project capacity rule.
- Basic Admin Configuration frontend shell.
- Backend and frontend tests for Phase 01 behavior.

## Changed Backend Files

- `backend/app/main.py`
- `backend/app/api/deps.py`
- `backend/app/api/routes/auth.py`
- `backend/app/api/routes/users.py`
- `backend/app/api/routes/customers.py`
- `backend/app/api/routes/projects.py`
- `backend/app/api/routes/project_ownership.py`
- `backend/app/models/__init__.py`
- `backend/app/models/mixins.py`
- `backend/app/models/user.py`
- `backend/app/models/customer.py`
- `backend/app/models/project.py`
- `backend/app/models/project_ownership.py`
- `backend/app/schemas/__init__.py`
- `backend/app/schemas/user.py`
- `backend/app/schemas/customer.py`
- `backend/app/schemas/project.py`
- `backend/app/schemas/project_ownership.py`
- `backend/app/services/__init__.py`
- `backend/app/services/rbac.py`
- `backend/app/services/ownership.py`
- `backend/alembic/env.py`
- `backend/alembic/versions/20260519_0001_phase_01_rbac_foundation.py`

## Changed Frontend Files

- `frontend/src/App.tsx`
- `frontend/src/styles.css`

## Changed Tests

- `backend/tests/conftest.py`
- `backend/tests/test_phase_01_rbac.py`
- `frontend/src/App.test.tsx`

Additional scenarios were added for bootstrap admin creation, first-user validation, duplicate email rejection, current-user simulation, non-admin mutation blocking, wrong-role ownership rejection, and customer visibility filtering.

## Migrations Added

- `20260519_0001_phase_01_rbac_foundation.py`
  - Creates `users`.
  - Creates `customers`.
  - Creates `projects`.
  - Creates `project_ownership`.
  - Adds unique user email index.
  - Adds role check constraint.
  - Adds unique project ownership constraint.
  - Adds ownership and project lookup indexes.

## API Endpoints Added Or Changed

- Added `GET /auth/current-user`.
- Added users, customers, projects, and project ownership endpoints listed in the implementation doc.
- Existing `GET /health` remains unchanged.

## RBAC Impact

- Admin can read and mutate Phase 01 configuration resources.
- VP, Project Director, PM, and DL can read only assigned projects and related customers/ownership records.
- Backend query filtering is implemented server-side.
- Frontend includes role-aware UI foundations, but backend remains the enforcement source.

## Scoring Impact

- None.
- Completed project state is stored for later scoring exclusion, but scoring is not implemented in Phase 01.

## Known Limitations

- Real authentication is not implemented; `X-User-Id` is a temporary current-user simulation.
- Frontend uses static/mock data and does not yet call the backend APIs.
- No delete endpoints were added; this phase uses minimal admin CRUD-style create/read/update.
- Project creation does not require ownership in the same request. Ownership is enforced through the project ownership resource.
- Docker services were config-validated with backend/frontend services included, but not started during this validation run because the Docker daemon was unavailable.

## Test Commands Run

- `..\.venv\Scripts\python.exe -m pytest`
- `npm run typecheck`
- `npm run lint`
- `npm test`
- `docker compose config`
- `docker compose build`
- `..\.venv\Scripts\python.exe -m alembic heads`
- `..\.venv\Scripts\python.exe -m alembic upgrade head --sql`
- `..\.venv\Scripts\python.exe -c "from app.main import app; print(app.title); print(len(app.routes))"`
- `npm run build`

## Test Results

- Backend pytest: passed, `19 passed`.
- Frontend typecheck: passed.
- Frontend lint: passed.
- Frontend tests: passed, `4 passed`.
- Docker Compose config: passed with `postgres`, `redis`, `backend`, and `frontend` services.
- Docker Compose build: blocked in this environment because the Docker daemon/pipe was unavailable after an escalated retry.
- Alembic heads: passed, `20260519_0001 (head)`.
- Alembic offline upgrade SQL generation: passed.
- FastAPI import validation: passed, printed `Customer Health Projection Agent API` and `22` routes.
- Frontend build: passed.
