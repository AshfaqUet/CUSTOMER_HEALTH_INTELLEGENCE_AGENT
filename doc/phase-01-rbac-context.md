# Phase 01 RBAC Context

## Scope

Phase 01 implements the foundation for identity, role-based project access, customers, projects, and project ownership.

The backend remains FastAPI with SQLAlchemy, Alembic, PostgreSQL-oriented migrations, and pytest. Real login/session auth is not implemented yet; this phase uses a testable `X-User-Id` current-user simulation.

## Included

- Users with one role per user.
- Customers.
- Projects belonging to customers.
- Project ownership with exactly one VP, Project Director, PM, and DL per ownership record.
- Backend RBAC filtering for project/customer/ownership reads.
- Admin-only configuration mutations.
- Delivery Lead active-project capacity blocking.
- Basic Admin Configuration frontend shell.
- Backend and frontend regression tests.

## Excluded

- Real authentication provider, password login, token issuance, or sessions.
- GitHub ingestion.
- Deliverables.
- AI analysis.
- Human review.
- Scoring and score history.
- Full Customer Health Dashboard tabs.
- Post-MVP sources.

## Role Rules Implemented

- Admin can access all customers, projects, users, and ownership records.
- VP can access projects where assigned as VP.
- Project Director can access projects where assigned as Project Director.
- PM can access projects where assigned as PM.
- DL can access projects where assigned as DL.
- DL assignment is blocked when the DL is already assigned to another non-completed project.
- Completed projects do not consume DL active-project capacity.
