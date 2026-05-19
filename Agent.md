# Agent.md - Customer Health Projection Agent

## 0. Purpose of this file

This file is the operating guide for Codex or any coding agent working on the Customer Health Projection Agent project.

Every implementation prompt must follow this file unless the user explicitly changes the product direction. Treat this file as the MVP source of truth.

The project is an AI-assisted web application that predicts customer escalation risk and current health from mapped project signals. The MVP focuses on GitHub and deliverables only. It must keep every health score explainable by linking score changes back to original processed events.

Recommended location in the repository:

```text
/Agent.md
```

If the coding environment expects `AGENTS.md`, create a copy at:

```text
/AGENTS.md
```

Do not remove or ignore this file when implementing features.

---

## 1. Product summary

### 1.1 Product name

Customer Health Projection Agent.

### 1.2 Core goal

Build an AI web application that detects early escalation risk signals before a customer formally escalates.

The system must:

1. Ingest configured customer-facing project signals.
2. Identify negative sentiment, repeated issues, blockers, and delivery risk.
3. Calculate deterministic health scores.
4. Show customers and projects in risk order.
5. Preserve evidence for every score contribution.
6. Allow human review for low-confidence AI results.
7. Store score history and trend data.

### 1.3 MVP primary output

The MVP primary screen is:

```text
Customer Health Dashboard
```

The Customer Health Dashboard must have multiple tabs/views so users can switch between customer, project, source, evidence, trend, and review contexts.

### 1.4 MVP tabs

Required MVP tabs:

```text
Customer Health
Project Health
GitHub Signals
Deliverables
Evidence / Events
Score History / Trends
Human Review
Admin Configuration
```

The main dashboard must sort customers and projects by highest risk first.

Since lower scores mean higher risk, sort by:

```text
health_score ascending
```

### 1.5 MVP data sources

MVP sources:

```text
GitHub
Deliverables
```

Post-MVP sources:

```text
Gmail / Email
Jira
Meeting notes
Other conversations
Slack / Teams notifications
Email notifications
Weekly reports
Advanced forecasting
GitHub webhooks
```

Do not implement post-MVP sources unless the user explicitly asks for that phase.

---

## 2. Fixed MVP decisions

These are final discovery decisions and must be respected.

### 2.1 Dashboard and scoring

```text
Primary MVP screen: Customer Health Dashboard
Default score: 8.0
Default score label: required
Score history/trend: included in MVP
Completed projects: excluded from active health calculation
```

Default score label example:

```text
8.0 Healthy - Default score, no analyzed risk signals yet
```

### 2.2 Source weights

Admin can configure only global source weight percentages in MVP.

Default source weights:

```text
GitHub: 40%
Deliverables: 60%
```

Validation rule:

```text
github_weight + deliverable_weight = 100%
```

Admin must not configure these in MVP:

```text
confidence threshold
max event penalty
recency decay
severity multipliers
urgency multipliers
customer impact multipliers
formula internals
```

Those belong to formula versions and backend code.

### 2.3 GitHub MVP scope

GitHub ingestion is polling-only in MVP.

No GitHub webhooks in MVP.

GitHub MVP event types:

```text
github_pr_comment
github_pr_review_comment
github_issue_comment
github_pr_reopened
github_repeated_issue_reference
```

Repeated issue window:

```text
30 days
```

Repeated issue threshold recommendation:

```text
Create a repeated issue signal when the same or similar customer risk appears 2 or more times within 30 days.
```

### 2.4 GitHub event eligibility

Only configured customer GitHub usernames affect sentiment and scoring.

Ignore for scoring:

```text
internal team comments
bots
dependabot
unmapped users
unmapped repositories
disabled customers
disabled projects
disabled repositories
completed projects
```

Skipped events may still be stored for audit/debugging if useful, but they must not affect sentiment or score.

### 2.5 GitHub prompts

Use separate AI prompt versions for each GitHub event type.

Required prompt versions:

```text
github_pr_comment_v1
github_pr_review_comment_v1
github_issue_comment_v1
github_pr_reopened_v1
github_repeated_issue_reference_v1
```

The response schema can be shared across event types, but the prompt instructions must be event-specific.

### 2.6 Deliverables MVP scope

Deliverables are entered by Admin through application forms.

Simple MVP statuses:

```text
not_started
in_progress
blocked
completed
cancelled
```

Blocked deliverable scoring must depend on priority and due date. It must not always force the score to 3.

### 2.7 Human review

Low-confidence or review-required AI results must appear in Human Review.

Human review permissions:

```text
Admin: can review all projects
PM: can review assigned projects
DL: can review assigned project
VP: view only
Project Director: view only
```

First approval finalizes the review item.

Editing a reviewed response does not affect scoring until a reviewer clicks:

```text
Approve for scoring
```

After approval, the review item is locked in MVP.

### 2.8 AI result edit rule

The raw AI response must never be overwritten.

Use this model:

```text
Raw AI response = immutable audit record
Reviewed response = editable before approval
Scoring uses reviewed response only after approval
```

High-confidence results may be auto-approved for scoring according to backend formula rules.

Low-confidence results must not be scored until approved by Admin, PM, or DL.

### 2.9 RBAC and ownership

Roles:

```text
Admin
Vice President
Project Director
Project Manager
Delivery Lead
```

Each user has only one role.

Each active project has exactly one:

```text
VP
Project Director
Project Manager
Delivery Lead
```

Capacity rules:

```text
VP can supervise multiple projects.
Project Director can supervise multiple projects.
PM can supervise multiple projects.
DL can supervise only one active project.
```

If Admin tries to assign a DL who is already assigned to another active project, block the assignment in MVP.

Do not allow override in MVP.

---

## 3. AI agent limits and guardrails

The AI system and coding agents must follow these limits.

### 3.1 AI analysis limits

AI is used to extract signals, not to calculate final scores.

Required principle:

```text
AI extracts signals. Backend calculates scores.
```

AI may produce:

```text
sentiment
sentiment_score
risk_detected
risk_category
urgency
severity
customer_impact
summary
evidence_excerpt
recommended_action
confidence
requires_human_review
```

AI must not directly set:

```text
customer health score
project health score
source health score
final risk ranking
score contribution value
formula version
```

Those are backend scoring responsibilities.

### 3.2 Mapping limits

Never score unmapped events.

Before analysis and scoring, always check:

```text
customer mapping
project mapping
repository mapping
source enabled flag
customer enabled flag
project enabled flag
author identity
author type
project completion status
```

Do not let internal comments, bot activity, or unmapped customer activity affect sentiment.

### 3.3 Content storage rule

MVP may store full GitHub event content and raw source payloads so the system can show which events were processed.

Every processed/scored event must also store:

```text
source reference or URL
author identifier
occurred_at timestamp
content excerpt
evidence excerpt
processing status
analysis status
score contribution link, if scored
```

### 3.4 Deterministic scoring rule

All health scores must be calculated by deterministic backend formulas.

Every score record must store:

```text
formula_version
calculation_run_id
calculated_at
score_status
source weights used
linked score contributions
```

Do not silently rewrite score history.

If the formula changes:

1. Create a new formula version.
2. Keep old snapshots.
3. Run explicit recomputation only when requested.
4. Store before/after values for recomputation jobs.

### 3.5 Human review limits

The review system must preserve audit history.

Do not mutate the raw AI response.

Allowed review decisions:

```text
approve_as_is
edit_response
approve_for_scoring
exclude_from_scoring
mark_duplicate
mark_not_customer_risk
```

Only these statuses are scoreable:

```text
analyzed_auto_approved
approved_for_scoring
```

These statuses are not scoreable:

```text
needs_human_review
review_in_progress
review_edited
excluded_from_scoring
marked_duplicate
analysis_failed
skipped
```

### 3.6 Regression safety rule

New feature additions must not break existing features.

Before completing any task, coding agents must:

1. Understand the existing behavior.
2. Update backend and frontend consistently.
3. Add or update tests.
4. Run relevant test suites.
5. Check RBAC impact.
6. Check scoring impact.
7. Check migrations and idempotency.
8. Update phase docs in `doc/`.

No task is complete until tests are added or updated.

### 3.7 Post-MVP extensibility rule

Design MVP modules with clear extension points for future sources.

Use generic concepts such as:

```text
source_type
source_object_type
source_events
analysis_status
score_type
score_contributions
prompt_versions
source_weights
```

Do not hardcode the system so tightly around GitHub that Gmail, Jira, or meeting notes become difficult to add later.

However, do not implement post-MVP features prematurely.

---

## 4. The three coding agents

Every feature request should be treated as a coordinated full-stack change unless the user explicitly says otherwise.

The three agents are:

```text
Backend Agent
Frontend Agent
Test and Quality Agent
```

### 4.1 Backend Agent

Responsible for backend implementation.

Scope:

```text
Python backend
API design
RBAC enforcement
PostgreSQL models
migrations
Celery jobs
Redis queue integration
GitHub polling
AI provider abstraction
prompt versions
analysis pipeline
human review workflow
scoring engine
score history/trends
audit logs
backend tests
```

Rules:

1. Enforce permissions in the backend, not only the frontend.
2. Keep event processors idempotent.
3. Use database constraints where appropriate.
4. Store raw AI response separately from reviewed response.
5. Preserve score history.
6. Keep scoring deterministic and formula-versioned.
7. Do not score disabled, unmapped, internal, bot, or completed-project events.
8. Use migrations for schema changes.
9. Add tests for each backend change.

### 4.2 Frontend Agent

Responsible for React implementation.

Scope:

```text
React UI
routing
state management
API integration
dashboard screens
admin configuration screens
GitHub signal views
deliverable screens
evidence views
score trend charts
human review UI
role-based UI visibility
frontend tests
```

Rules:

1. Build the Customer Health Dashboard as the primary MVP screen.
2. Show default score label clearly.
3. Sort risky customers and projects first.
4. Show source breakdown and evidence links.
5. Show score history/trend in MVP.
6. Restrict review actions in UI to Admin, PM, and DL.
7. Show view-only review state for VP and Project Director.
8. Do not rely on frontend-only security; backend must enforce access.
9. Add tests for each UI change.

### 4.3 Test and Quality Agent

Responsible for preventing regressions and validating implementation quality.

Scope:

```text
unit tests
integration tests
API tests
RBAC tests
Celery job tests
scoring tests
AI response schema tests
frontend component tests
end-to-end smoke tests
regression checks
validation reports
```

Rules:

1. Every feature must include tests.
2. Every bug fix must include a regression test.
3. Test the happy path and the blocked/forbidden path.
4. Test idempotency for ingestion jobs.
5. Test source eligibility filters.
6. Test score formulas and score history creation.
7. Test human review locking after first approval.
8. Test DL assignment blocking.
9. Test completed project exclusion.
10. Test default score label behavior.

### 4.4 Agent handoff protocol

For every feature prompt, use this flow:

```text
1. Backend Agent identifies backend changes.
2. Frontend Agent identifies frontend changes.
3. Test and Quality Agent identifies required tests.
4. Implement backend.
5. Implement frontend.
6. Implement tests.
7. Run validation.
8. Update doc/ phase context files.
9. Provide final summary with changed files and test results.
```

No feature should be considered done if it only changes backend or only changes frontend when the product behavior requires both.

---

## 5. Recommended technology stack

### 5.1 Frontend

```text
React
TypeScript recommended
Vite or project-selected React tooling
API client layer
component tests
```

### 5.2 Backend

```text
Python
Django REST Framework or FastAPI
Celery
Redis
PostgreSQL
pytest
```

Discovery recommendation: Django REST Framework is a strong MVP choice because this product has many admin CRUD screens, RBAC flows, and configuration models.

If the repository already uses FastAPI or another Python framework, follow the existing framework instead of switching without user approval.

### 5.3 Background jobs

```text
Celery workers
Celery Beat or scheduler
Redis broker
PostgreSQL persistence
```

### 5.4 AI providers

AI provider must be configurable.

Supported providers:

```text
OpenAI
Claude
Ollama fallback
```

Store provider metadata for every AI analysis:

```text
provider
model_name
prompt_version
response_schema_version
created_at
```

---

## 6. Recommended repository structure

Use the existing repository structure if it already exists. If starting fresh, prefer this shape:

```text
/
  Agent.md
  README.md
  doc/
    project-overview.md
    architecture.md
    rbac.md
    scoring.md
    ai-analysis.md
    phase-00-foundation-context.md
    phase-00-foundation-validation.md
  backend/
    apps/
      users/
      customers/
      projects/
      ownership/
      github_integration/
      deliverables/
      source_events/
      ai_analysis/
      human_review/
      scoring/
      dashboard/
      audit/
    tests/
  frontend/
    src/
      app/
      api/
      components/
      pages/
      features/
        customer-health/
        project-health/
        github-signals/
        deliverables/
        evidence-events/
        score-trends/
        human-review/
        admin-config/
      tests/
```

If using a monorepo, keep backend and frontend clearly separated.

---

## 7. Core domain model

### 7.1 Required MVP tables/models

Use framework-specific naming conventions, but preserve these concepts.

```text
users
customers
projects
project_ownership
github_repositories
project_github_repositories
customer_github_identities
deliverables
source_events
derived_event_links
prompt_versions
event_ai_analysis_raw
reviewed_event_analysis
score_formula_versions
score_calculation_runs
score_snapshots
current_scores
score_contributions
system_source_weights
audit_logs
```

### 7.2 Users

Fields:

```text
id
name
email
role
is_active
created_at
updated_at
```

Valid roles:

```text
admin
vice_president
project_director
project_manager
delivery_lead
```

A user has exactly one role.

### 7.3 Customers

Fields:

```text
id
name
health_calculation_enabled
priority
status
created_at
updated_at
```

### 7.4 Projects

Fields:

```text
id
customer_id
name
health_calculation_enabled
status
importance
is_completed
completed_at
created_at
updated_at
```

Completed projects are excluded from active scoring.

### 7.5 Project ownership

Fields:

```text
id
project_id
vp_user_id
project_director_user_id
project_manager_user_id
delivery_lead_user_id
created_at
updated_at
```

Validation:

```text
VP, Project Director, PM, and DL are required for each active project.
DL must not be assigned to more than one active project.
```

### 7.6 GitHub repositories

Fields:

```text
id
repo_owner
repo_name
repo_url
github_repo_id
is_active
created_at
updated_at
```

### 7.7 Project GitHub repositories

Fields:

```text
id
project_id
github_repository_id
sentiment_enabled
last_synced_at
last_successful_sync_at
last_sync_status
last_error
created_at
updated_at
```

### 7.8 Customer GitHub identities

Fields:

```text
id
customer_id
project_id
github_username
display_name
identity_type
is_active
created_at
updated_at
```

Valid identity types:

```text
customer
internal
bot
unknown
```

Only `customer` identities are eligible for sentiment and scoring.

### 7.9 Deliverables

Fields:

```text
id
customer_id
project_id
name
description
due_date
status
priority
owner_user_id
completed_at
cancelled_at
created_by_user_id
created_at
updated_at
```

Valid statuses:

```text
not_started
in_progress
blocked
completed
cancelled
```

Valid priorities:

```text
low
medium
high
critical
```

### 7.10 Source events

All source inputs must be normalized into source events.

Fields:

```text
id
customer_id
project_id
source_type
source_object_type
external_source_id
deduplication_key
source_url
author_identifier
author_display_name
author_type
occurred_at
ingested_at
content_text
content_excerpt
content_hash
raw_payload_json
is_mapped
is_eligible_for_analysis
processing_status
analysis_status
created_at
updated_at
```

MVP source types:

```text
github
deliverable
```

MVP GitHub source object types:

```text
github_pr_comment
github_pr_review_comment
github_issue_comment
github_pr_reopened
github_repeated_issue_reference
```

Deliverable source object types:

```text
deliverable_created
deliverable_updated
deliverable_overdue
deliverable_blocked
deliverable_completed
deliverable_cancelled
```

Required unique constraint:

```text
unique(source_type, deduplication_key)
```

### 7.11 Derived event links

Use this table to link repeated issue derived events back to original evidence.

Fields:

```text
id
derived_source_event_id
original_source_event_id
relationship_type
created_at
```

Relationship type example:

```text
repeated_issue_evidence
```

### 7.12 Prompt versions

Fields:

```text
id
name
source_type
source_object_type
version
prompt_text
response_schema_version
is_active
created_at
updated_at
```

Required MVP prompt names:

```text
github_pr_comment_v1
github_pr_review_comment_v1
github_issue_comment_v1
github_pr_reopened_v1
github_repeated_issue_reference_v1
```

### 7.13 Raw AI analysis

Fields:

```text
id
source_event_id
provider
model_name
prompt_version
response_schema_version
sentiment
sentiment_score
risk_detected
risk_category
urgency
severity
customer_impact
summary
evidence_excerpt
recommended_action
confidence
requires_human_review
raw_ai_response_json
created_at
```

This record is immutable.

### 7.14 Reviewed event analysis

Fields:

```text
id
source_event_id
raw_ai_analysis_id
reviewed_by_user_id
review_status
sentiment
sentiment_score
risk_detected
risk_category
urgency
severity
customer_impact
summary
evidence_excerpt
recommended_action
include_in_scoring
approved_for_scoring
approved_by_user_id
approved_at
locked_at
review_notes
created_at
updated_at
```

Once `locked_at` is set, no edits are allowed in MVP.

### 7.15 Score formula versions

Fields:

```text
id
version
description
config_json
is_active
created_at
```

### 7.16 Score calculation runs

Fields:

```text
id
formula_version
started_at
finished_at
status
triggered_by
error_message
created_at
```

### 7.17 Score snapshots

Store score history here.

Fields:

```text
id
entity_type
entity_id
score_type
score_value
risk_level
score_status
formula_version
calculation_run_id
calculated_at
```

Entity types:

```text
customer
project
source
deliverable
```

Score types:

```text
customer_overall
project_overall
github_source
deliverable_source
deliverable_health
```

### 7.18 Current scores

Store latest score here for fast dashboard loading.

Fields:

```text
id
entity_type
entity_id
score_type
score_value
risk_level
score_status
formula_version
latest_snapshot_id
updated_at
```

### 7.19 Score contributions

Fields:

```text
id
score_snapshot_id
source_event_id
raw_ai_analysis_id
reviewed_event_analysis_id
contribution_value
contribution_direction
reason
formula_version
created_at
```

Contribution direction:

```text
positive
negative
neutral
```

Every non-default score change must be explainable using this table.

### 7.20 System source weights

Fields:

```text
id
github_weight_percentage
deliverable_weight_percentage
is_active
created_at
updated_at
```

Validation:

```text
github_weight_percentage + deliverable_weight_percentage = 100
```

---

## 8. AI response schema

All GitHub AI prompts should return the same normalized JSON shape.

```json
{
  "sentiment": "negative",
  "sentiment_score": -0.78,
  "risk_detected": true,
  "risk_category": "technical_blocker",
  "risk_reason_codes": ["blocking_release", "repeated_issue"],
  "related_deliverable_id": null,
  "related_deliverable_name": null,
  "urgency": "high",
  "severity": "high",
  "customer_impact": "high",
  "summary": "Customer says the issue is still blocking their release.",
  "evidence_excerpt": "This is still blocking our release.",
  "recommended_action": "Assign a technical owner and reply with a clear ETA.",
  "confidence": 0.91,
  "requires_human_review": false
}
```

Valid values:

```text
sentiment: positive, neutral, negative
urgency: low, medium, high
severity: low, medium, high
customer_impact: low, medium, high
```

Invalid or incomplete JSON must not be scored automatically.

---

## 9. Scoring model v1

### 9.1 Score ranges

```text
0-2   Critical
2-4   High Risk
4-6   Watch
6-8   Healthy
8-10  Strong
```

Special case:

```text
Exactly 8.0 with no analyzed risk signals = Healthy - Default score, no analyzed risk signals yet
```

### 9.2 Project score

Default formula:

```text
project_score = github_score * 0.40 + deliverable_score * 0.60
```

Use Admin-configured source percentages from `system_source_weights`.

If a source is disabled or unavailable, normalize across enabled sources only.

### 9.3 Customer score

Customer score is the average of active project scores.

```text
customer_score = average(active_project_scores)
```

Exclude completed projects.

If a customer has no active projects with calculated signals, use default:

```text
8.0 Healthy - Default score, no analyzed risk signals yet
```

### 9.4 GitHub score

Start from default source score:

```text
github_score = 8.0
```

Then apply approved negative event penalties and recovery credits.

```text
github_score = clamp(8.0 - negative_event_penalties + recovery_credits, 0, 10)
```

Only use events that are:

```text
mapped
eligible
customer-authored or customer-linked
analyzed_auto_approved or approved_for_scoring
not duplicate
not excluded
not from completed projects
```

### 9.5 GitHub event penalty

For an approved GitHub signal:

```text
event_penalty =
  negative_sentiment_strength
  * severity_multiplier
  * urgency_multiplier
  * customer_impact_multiplier
  * confidence_or_review_multiplier
  * recency_multiplier
```

Where:

```text
negative_sentiment_strength = max(0, -sentiment_score)
```

Suggested formula internals for v1:

```text
severity: low=0.75, medium=1.00, high=1.35
urgency: low=0.85, medium=1.00, high=1.20
customer_impact: low=0.85, medium=1.00, high=1.25
recency: 0-7 days=1.00, 8-30 days=0.60, 31-90 days=0.30, 90+ days=0.10
max_single_event_penalty=2.0
max_daily_github_penalty=3.0
```

Do not expose these internals as Admin configuration in MVP.

### 9.6 Deliverable score

Deliverables do not need AI in MVP. Score them deterministically.

Non-blocked deliverable scoring:

```text
Completed on time: 10
Completed late: 8
Not started, not near due date: 8
In progress, not near due date: 8
Due within 3 days: 7
1-3 days late: 6
4-7 days late: 4.5
8-14 days late: 3
15+ days late: 1.5
Cancelled: excluded
```

Blocked deliverable scoring depends on priority and due date:

```text
Blocked, not near due date:
  low=7.0, medium=6.0, high=5.0, critical=4.0

Blocked, due within 3 days:
  low=6.0, medium=5.0, high=4.0, critical=3.0

Blocked, 1-7 days late:
  low=5.0, medium=4.0, high=3.0, critical=2.0

Blocked, 8+ days late:
  low=4.0, medium=3.0, high=2.0, critical=1.0
```

Deliverable source score:

```text
deliverable_score = weighted_average(deliverable_scores, priority_weight)
```

Priority weights:

```text
low=0.75
medium=1.00
high=1.25
critical=1.50
```

### 9.7 Score history

Every scoring run must:

1. Create `score_calculation_run`.
2. Create `score_snapshots`.
3. Create `score_contributions`.
4. Update `current_scores`.

Never update historical snapshots in place.

---

## 10. MVP job flows

### 10.1 Admin setup flow

```text
Admin creates customer
Admin creates project
Admin assigns VP, Project Director, PM, and DL
System blocks DL if already assigned to another active project
Admin maps GitHub repositories
Admin adds customer GitHub usernames
Admin adds deliverables
Admin configures global source weight percentages
System starts polling and scoring jobs
```

### 10.2 GitHub polling flow

```text
Scheduler enqueues GitHub polling job
Worker loads active project repositories
Worker skips completed projects
Worker fetches PR comments, review comments, issue comments, PR reopened events
Worker checks repository and project mapping
Worker checks author identity
Worker builds stable deduplication key
Worker upserts source_event
Worker marks event as eligible or skipped
```

### 10.3 AI analysis flow

```text
Worker finds pending eligible GitHub source events
Worker selects prompt version by source_object_type
Worker calls configured AI provider
Worker validates response JSON
Worker stores immutable raw AI response
If result is high confidence and valid, mark analyzed_auto_approved
If low confidence or review required, mark needs_human_review
Invalid responses become analysis_failed
```

### 10.4 Human review flow

```text
Admin, PM, or DL opens Human Review
Reviewer views raw AI result
Reviewer can create or edit reviewed response
Reviewer clicks Approve for scoring
System locks review item
System marks source event approved_for_scoring
First approval finalizes the review item
```

### 10.5 Repeated issue detection flow

```text
Worker scans last 30 days of approved or reviewable GitHub risk events
Worker groups similar risks by project, repo, risk category, issue/PR reference, and topic hash
If 2 or more similar risks exist, create github_repeated_issue_reference event
Worker links derived event to original events using derived_event_links
AI analyzes repeated issue event with github_repeated_issue_reference_v1 prompt
```

### 10.6 Deliverable scoring flow

```text
Worker loads active project deliverables
Worker skips cancelled deliverables
Worker checks status, priority, due date, completed_at
Worker calculates deliverable score
Worker aggregates deliverable source score
```

### 10.7 Scoring flow

```text
Create score calculation run
Calculate GitHub source score
Calculate deliverable source score
Apply global source weights
Calculate project score
Calculate customer score from active project scores
Create score snapshots
Create score contributions
Update current scores
Expose latest and historical scores to dashboard
```

---

## 11. RBAC rules

### 11.1 Visibility rules

Admin:

```text
Can see all customers, projects, scores, events, reviews, raw AI responses, reviewed responses, and settings.
```

VP:

```text
Can see only projects where they are assigned as VP.
Can view dashboard, evidence, trends, and review items.
Cannot approve human review.
```

Project Director:

```text
Can see only projects where they are assigned as Project Director.
Can view dashboard, evidence, trends, and review items.
Cannot approve human review.
```

PM:

```text
Can see only projects where they are assigned as PM.
Can review and approve human review items for assigned projects.
```

DL:

```text
Can see only the project where they are assigned as DL.
Can review and approve human review items for assigned project.
```

### 11.2 Backend enforcement

All APIs must enforce RBAC in backend querysets/services.

Do not rely on frontend hiding alone.

### 11.3 Review permissions

Only these roles can approve for scoring:

```text
admin
project_manager
delivery_lead
```

### 11.4 Raw AI side-by-side view

Admin can see raw AI response and reviewed response side by side.

Other roles should see only what product permissions allow. If uncertain, restrict raw AI side-by-side view to Admin only.

---

## 12. API surface guidelines

Use existing API conventions if present. If starting fresh, design around these resources.

### 12.1 Admin/config APIs

```text
/users
/customers
/projects
/project-ownership
/source-weights
/github/repositories
/github/project-repositories
/github/customer-identities
/deliverables
```

### 12.2 Dashboard APIs

```text
/dashboard/customer-health
/dashboard/project-health
/dashboard/source-breakdown
/dashboard/evidence-events
/dashboard/score-trends
```

### 12.3 Review APIs

```text
/human-review/items
/human-review/items/{id}
/human-review/items/{id}/edit
/human-review/items/{id}/approve-for-scoring
/human-review/items/{id}/exclude
/human-review/items/{id}/mark-duplicate
```

### 12.4 Source event APIs

```text
/source-events
/source-events/{id}
/source-events/{id}/analysis
/source-events/{id}/score-contributions
```

### 12.5 Scoring APIs

```text
/scores/current
/scores/history
/scores/contributions
/scoring/runs
```

---

## 13. Frontend behavior requirements

### 13.1 Customer Health tab

Must show:

```text
customer name
current health score
risk label
score status/default label
active project count
highest-risk project
latest score change
trend indicator
```

Sort by:

```text
health_score ascending
```

### 13.2 Project Health tab

Must show:

```text
project name
customer
current score
risk label
GitHub score
Deliverable score
source weights used
score status
owner chain: VP, Project Director, PM, DL
```

Completed projects hidden by default.

### 13.3 GitHub Signals tab

Must show:

```text
event type
repository
PR/issue reference
author
analysis status
sentiment
risk category
severity
urgency
customer impact
score impact if scored
source URL
```

### 13.4 Deliverables tab

Must show:

```text
deliverable name
project
status
priority
due date
days until due or days overdue
calculated deliverable score
score reason
```

### 13.5 Evidence / Events tab

Must show all processed source events that the user can access.

Each event should show:

```text
source type
source object type
author
occurred at
processing status
analysis status
content or excerpt
source URL
score contribution
```

### 13.6 Score History / Trends tab

Must show:

```text
customer score over time
project score over time
source score over time
score change reasons
```

Default trend range recommendation:

```text
30 days
```

Optional filters:

```text
7 days
30 days
90 days
custom
```

### 13.7 Human Review tab

Must show low-confidence or review-required events.

Allowed actions for Admin, PM, DL:

```text
edit reviewed response
approve for scoring
exclude from scoring
mark duplicate
mark not customer risk
```

VP and Project Director view only.

When approval happens:

```text
lock the review item
prevent further editing in MVP
show approved_by and approved_at
```

### 13.8 Admin Configuration tab

Must allow Admin to configure:

```text
users
customers
projects
ownership mapping
GitHub repositories
customer GitHub usernames
deliverables
source weights as percentages
customer/project/source enable flags
```

---

## 14. Development phases

Each phase must create or update Markdown context files in the `doc/` folder.

Use this pattern:

```text
doc/phase-XX-<phase-name>-context.md
doc/phase-XX-<phase-name>-implementation.md
doc/phase-XX-<phase-name>-validation.md
```

If a phase is split into multiple features, add feature-specific docs:

```text
doc/phase-XX-<phase-name>-<feature-name>.md
```

### Phase 00 - Foundation and project setup

Goal:

```text
Create project skeleton, shared conventions, environment setup, base docs, CI/test commands.
```

Deliverables:

```text
backend app skeleton
frontend app skeleton
PostgreSQL/Redis local setup
base README
Agent.md copied to repo root
initial doc/ files
basic test commands
lint/typecheck/build commands
```

Docs:

```text
doc/phase-00-foundation-context.md
doc/phase-00-foundation-implementation.md
doc/phase-00-foundation-validation.md
```

### Phase 01 - Auth, users, RBAC, customers, projects, ownership

Goal:

```text
Implement core identity, project hierarchy, and access rules.
```

Deliverables:

```text
users and roles
customer CRUD
project CRUD
project ownership mapping
DL one-active-project blocking
backend RBAC filters
frontend admin screens
basic dashboard shell
RBAC tests
```

Docs:

```text
doc/phase-01-rbac-context.md
doc/phase-01-rbac-implementation.md
doc/phase-01-rbac-validation.md
```

### Phase 02 - Deliverables and deterministic deliverable health

Goal:

```text
Implement Admin-entered deliverables and deterministic deliverable scoring.
```

Deliverables:

```text
deliverable CRUD
simple statuses
priority support
due date handling
blocked scoring by priority and due date
deliverable score snapshots
deliverables tab
backend and frontend tests
```

Docs:

```text
doc/phase-02-deliverables-context.md
doc/phase-02-deliverables-implementation.md
doc/phase-02-deliverables-validation.md
```

### Phase 03 - GitHub configuration and polling ingestion

Goal:

```text
Implement GitHub repository mapping, customer GitHub identities, polling ingestion, and event deduplication.
```

Deliverables:

```text
GitHub repository config
project repository mapping
customer GitHub usernames
polling worker
source_events table
stable deduplication keys
eligibility checks
skipped event statuses
GitHub Signals tab initial view
ingestion idempotency tests
```

Docs:

```text
doc/phase-03-github-ingestion-context.md
doc/phase-03-github-ingestion-implementation.md
doc/phase-03-github-ingestion-validation.md
```

### Phase 04 - AI provider abstraction, prompts, and GitHub analysis

Goal:

```text
Analyze eligible GitHub events using configurable AI providers and event-specific prompts.
```

Deliverables:

```text
AI provider abstraction
OpenAI provider
Claude provider
Ollama fallback provider
prompt_versions table
separate GitHub prompt versions
response JSON validation
raw AI analysis storage
analysis status updates
AI analysis tests
```

Docs:

```text
doc/phase-04-ai-analysis-context.md
doc/phase-04-ai-analysis-implementation.md
doc/phase-04-ai-analysis-validation.md
```

### Phase 05 - Human review workflow

Goal:

```text
Implement review workflow for low-confidence or review-required AI results.
```

Deliverables:

```text
reviewed_event_analysis table
Human Review tab
Admin/PM/DL review permissions
VP/PD view-only behavior
edit reviewed response
approve for scoring action
first approval finalizes
review locking
review audit fields
review tests
```

Docs:

```text
doc/phase-05-human-review-context.md
doc/phase-05-human-review-implementation.md
doc/phase-05-human-review-validation.md
```

### Phase 06 - Repeated issue detection

Goal:

```text
Detect repeated customer issues across GitHub events within a 30-day window.
```

Deliverables:

```text
30-day repeated issue job
derived_event_links
github_repeated_issue_reference events
repeated issue AI prompt
links to original evidence
repeated issue tests
```

Docs:

```text
doc/phase-06-repeated-issues-context.md
doc/phase-06-repeated-issues-implementation.md
doc/phase-06-repeated-issues-validation.md
```

### Phase 07 - Scoring engine, source weights, and score history

Goal:

```text
Implement deterministic formula-versioned scoring and score snapshots.
```

Deliverables:

```text
system source weights
score_formula_versions
score_calculation_runs
score_snapshots
current_scores
score_contributions
GitHub score calculation
deliverable score aggregation
project score calculation
customer score calculation
default 8.0 behavior
completed project exclusion
score history APIs
scoring tests
```

Docs:

```text
doc/phase-07-scoring-context.md
doc/phase-07-scoring-implementation.md
doc/phase-07-scoring-validation.md
```

### Phase 08 - Customer Health Dashboard and trends

Goal:

```text
Build the full MVP dashboard experience.
```

Deliverables:

```text
Customer Health tab
Project Health tab
GitHub Signals tab
Deliverables tab
Evidence / Events tab
Score History / Trends tab
Human Review tab integration
Admin Configuration tab integration
risk-first sorting
default score label
trend charts
evidence drill-down
dashboard tests
```

Docs:

```text
doc/phase-08-dashboard-context.md
doc/phase-08-dashboard-implementation.md
doc/phase-08-dashboard-validation.md
```

### Phase 09 - Hardening, observability, and MVP release

Goal:

```text
Prepare MVP for reliable use.
```

Deliverables:

```text
error handling
job retry behavior
job run logs
audit logs
API pagination
performance checks
security review
seed/demo data
release validation
end-to-end smoke tests
```

Docs:

```text
doc/phase-09-hardening-context.md
doc/phase-09-hardening-implementation.md
doc/phase-09-hardening-validation.md
```

### Post-MVP phases

Do not implement these during MVP unless specifically requested.

```text
Post-MVP 01 - Gmail connected mailbox and email sentiment
Post-MVP 02 - Jira boards and issue health
Post-MVP 03 - Meeting notes and conversation sources
Post-MVP 04 - External notifications through Slack, Teams, and email
Post-MVP 05 - Weekly reports and executive summaries
Post-MVP 06 - GitHub webhooks and near-real-time ingestion
Post-MVP 07 - Advanced forecasting and escalation playbooks
```

---

## 15. Documentation requirements

### 15.1 Required docs

Maintain these core docs:

```text
doc/project-overview.md
doc/architecture.md
doc/rbac.md
doc/scoring.md
doc/ai-analysis.md
doc/github-ingestion.md
doc/deliverables.md
doc/human-review.md
doc/dashboard.md
doc/post-mvp-roadmap.md
```

### 15.2 Phase docs

After each phase, create side-by-side context docs in `doc/`.

Every phase validation doc must include:

```text
implemented scope
changed backend files
changed frontend files
changed tests
migrations added
API endpoints added/changed
RBAC impact
scoring impact
known limitations
test commands run
test results
```

### 15.3 Feature docs

For substantial features, add a feature context file:

```text
doc/feature-<feature-name>.md
```

It must include:

```text
problem
solution
backend changes
frontend changes
test coverage
RBAC impact
scoring impact
migration impact
rollout notes
```

---

## 16. Testing requirements

### 16.1 Backend tests

Required coverage areas:

```text
user roles
project visibility
DL one-active-project blocking
customer/project CRUD permissions
GitHub repo mapping
customer GitHub identity eligibility
GitHub ingestion deduplication
skipping bots/internal/unmapped users
source event status transitions
AI response JSON validation
raw AI immutability
human review permissions
first approval locks review
approved_for_scoring eligibility
source weights validation
scoring formulas
default 8.0 score behavior
completed project exclusion
score snapshot creation
current score update
score contribution links
repeated issue 30-day detection
```

### 16.2 Frontend tests

Required coverage areas:

```text
Customer Health dashboard sorting
8.0 default score label
role-based visible actions
Human Review actions for Admin/PM/DL
Human Review view-only for VP/PD
review item locked after approval
source breakdown rendering
score trend rendering
evidence event rendering
deliverable status display
blocked deliverable display
admin source weight validation
```

### 16.3 Integration tests

Required scenarios:

```text
Admin creates project and assigns ownership
Admin blocked from assigning busy DL
GitHub customer comment is ingested once
GitHub bot comment is skipped for scoring
GitHub customer comment is analyzed
Low-confidence analysis goes to review
PM approves review for scoring
Scoring run creates score history and current score
Dashboard shows updated score and evidence
Completed project is excluded from customer score
Repeated issue signal created after 2 similar risks within 30 days
```

### 16.4 Suggested commands

Use the repository's actual commands if they differ. If starting fresh, provide these scripts.

Backend:

```text
pytest
python manage.py check
python manage.py makemigrations --check --dry-run
```

Frontend:

```text
npm run lint
npm run typecheck
npm test
npm run build
```

End-to-end, if configured:

```text
npm run e2e
```

### 16.5 Bug fix rule

Every bug fix must include a regression test that fails before the fix and passes after the fix.

---

## 17. Implementation checklist for every prompt

When the user prompts Codex to implement something, follow this checklist.

### 17.1 Understand

```text
Read Agent.md
Read relevant doc/ files
Identify the phase and feature area
Identify MVP vs post-MVP scope
Identify affected roles
Identify affected source types
Identify scoring impact
```

### 17.2 Plan

```text
List backend changes
List frontend changes
List tests to add/update
List docs to update
List migrations needed
List risks/regressions
```

### 17.3 Implement

```text
Implement backend first if APIs/data are needed
Implement frontend against typed/validated API contracts
Implement tests with the change
Add migrations where needed
Update docs in doc/
```

### 17.4 Validate

```text
Run backend tests
Run frontend tests
Run lint/typecheck/build
Run targeted regression tests
Confirm RBAC behavior
Confirm scoring behavior
Confirm no post-MVP scope slipped in unintentionally
```

### 17.5 Report

Final response must include:

```text
summary of changes
files changed
migrations added
tests added/updated
test commands run
known limitations
next recommended step
```

---

## 18. Non-goals for MVP

Do not implement these in MVP unless the user explicitly changes scope:

```text
Gmail integration
Email sentiment
Jira integration
Meeting notes analysis
Slack notifications
Teams notifications
Email notifications
Weekly report generation
Customer-facing user access
GitHub webhooks
Advanced escalation playbooks
AI-generated final health score
Manual score override
Multiple roles per user
Multiple DLs per project
One DL on multiple active projects
Project-level source weight configuration
Admin editing formula internals through UI
```

---

## 19. Validation checklist for this Agent.md

This file satisfies the requested creation steps as follows.

### Step 1 - Understand the whole project

Covered by:

```text
Section 1 Product summary
Section 2 Fixed MVP decisions
Section 7 Core domain model
Section 10 MVP job flows
Section 14 Development phases
```

### Step 2 - Define the limits for AI agent

Covered by:

```text
Section 3 AI agent limits and guardrails
Section 8 AI response schema
Section 9 Scoring model v1
Section 18 Non-goals for MVP
```

### Step 3 - Design for post-MVP extensibility

Covered by:

```text
Section 3.7 Post-MVP extensibility rule
Section 7 generic source event and scoring models
Section 14 Post-MVP phases
Section 18 Non-goals for MVP
```

### Step 4 - Create 3 agents for FE, BE, and tests

Covered by:

```text
Section 4 The three coding agents
Backend Agent
Frontend Agent
Test and Quality Agent
```

### Step 5 - Prevent new features from creating bugs in existing features

Covered by:

```text
Section 3.6 Regression safety rule
Section 16 Testing requirements
Section 17 Implementation checklist
```

### Step 6 - Define phases for project development

Covered by:

```text
Section 14 Development phases
```

### Step 7 - Create Markdown files after each phase in doc/ folder

Covered by:

```text
Section 14 phase documentation file names
Section 15 Documentation requirements
```

---

## 20. Final instruction to coding agents

Build the MVP incrementally.

Do not skip RBAC, idempotency, auditability, score evidence, or tests.

The product is not complete when a score appears on screen. It is complete only when the score is explainable, permission-safe, backed by source evidence, stored historically, and covered by tests.
