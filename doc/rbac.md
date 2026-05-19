# RBAC

Phase 01 implements the first RBAC foundation with a simulated current-user dependency.

## Roles

- `admin`
- `vice_president`
- `project_director`
- `project_manager`
- `delivery_lead`

Each user has exactly one role.

## Current-User Simulation

Real authentication is not implemented yet. API tests and local clients can pass:

```text
X-User-Id: <user id>
```

The backend resolves that user and enforces role checks server-side.

## Implemented Visibility

- Admin can access all projects, customers, users, and ownership records.
- VP can access projects where assigned as VP.
- Project Director can access projects where assigned as Project Director.
- PM can access projects where assigned as PM.
- DL can access projects where assigned as DL.

Customer and project ownership list endpoints are filtered through the same project access rules.

## Implemented Mutation Rules

- Admin-only for users, customers, projects, and project ownership mutations.
- A project ownership row requires exactly one VP, Project Director, PM, and DL.
- Owner user IDs must reference active users with the expected role.
- A DL cannot be assigned to more than one active non-completed project.
- Completed projects do not consume DL active-project capacity.

## Not Yet Implemented

- Passwords, sessions, OAuth, JWTs, or SSO.
- Fine-grained permissions beyond Phase 01 resources.
- Human review permission actions.
- Scoring-specific permissions.
