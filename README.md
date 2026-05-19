# Customer Health Projection Agent

Development foundation for the Customer Health Projection Agent MVP.

The backend is intentionally built with FastAPI, SQLAlchemy, Alembic, Celery, Redis, and PostgreSQL. The frontend is React, TypeScript, and Vite. Current scope includes the Phase 00 foundation and Phase 01 identity/RBAC foundation only. GitHub polling, deliverables, AI analysis, scoring, human review, full dashboard business logic, and post-MVP integrations are not implemented yet.

## Repository Layout

```text
/
  AGENTS.md
  Agent.md
  docker-compose.yml
  .env.example
  backend/
  frontend/
  doc/
```

## Backend Setup

Create and activate the virtual environment from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

Install backend dependencies:

```powershell
python -m pip install -e "backend[dev]"
```

Copy backend environment defaults if needed:

```powershell
Copy-Item backend\.env.example backend\.env
```

Start PostgreSQL and Redis:

```powershell
docker compose up -d
```

Run FastAPI locally:

```powershell
cd backend
uvicorn app.main:app --reload
```

The API exposes:

```text
GET http://localhost:8000/health
```

Run backend tests:

```powershell
cd backend
pytest
```

Alembic commands:

```powershell
cd backend
alembic current
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

There are no domain migrations in Phase 00.

For Phase 01 database tables, run:

```powershell
cd backend
alembic upgrade head
```

## Frontend Setup

Install frontend dependencies:

```powershell
cd frontend
npm install
```

Run the frontend dev server:

```powershell
npm run dev
```

Run frontend checks:

```powershell
npm test
npm run typecheck
npm run lint
npm run build
```

## Local Services

Copy root environment defaults if needed:

```powershell
Copy-Item .env.example .env
```

Then start:

```powershell
docker compose up -d
```

Default local ports:

```text
PostgreSQL: 5432
Redis: 6379
FastAPI: 8000
Vite: 5173
```

## Full Stack Docker Compose

The full local development stack can run from the repository root:

```powershell
docker compose up --build
```

Open locally:

```text
Frontend: http://localhost:5173
Backend: http://localhost:8000
API docs: http://localhost:8000/docs
Health endpoint: http://localhost:8000/health
```

The backend container uses Docker service names:

```text
PostgreSQL: postgres:5432
Redis: redis:6379
```

Run migrations in Docker:

```powershell
docker compose run --rm backend alembic upgrade head
```

View logs:

```powershell
docker compose logs -f backend
docker compose logs -f frontend
```

Stop services:

```powershell
docker compose down
```

Stop services and remove named volumes:

```powershell
docker compose down -v
```

Run tests outside Docker:

```powershell
cd backend
pytest

cd ..\frontend
npm test
npm run typecheck
npm run lint
npm run build
```

Run tests inside Docker after images are built:

```powershell
docker compose run --rm backend pytest
docker compose run --rm frontend npm test
```

## MVP Scope Reminder

`AGENTS.md` is the source of truth. The app must continue to be built incrementally by phase, with backend enforcement, tests, validation, and docs updated for each phase.
