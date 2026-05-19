"""phase 01 rbac foundation

Revision ID: 20260519_0001
Revises:
Create Date: 2026-05-19 19:00:00
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260519_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

USER_ROLES = (
    "admin",
    "vice_president",
    "project_director",
    "project_manager",
    "delivery_lead",
)


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(f"role in {USER_ROLES}", name="ck_users_role"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("health_calculation_enabled", sa.Boolean(), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_customers_name"), "customers", ["name"], unique=False)

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("health_calculation_enabled", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("importance", sa.String(length=50), nullable=False),
        sa.Column("is_completed", sa.Boolean(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_projects_customer_id"), "projects", ["customer_id"], unique=False)
    op.create_index(op.f("ix_projects_name"), "projects", ["name"], unique=False)

    op.create_table(
        "project_ownership",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("vp_user_id", sa.Integer(), nullable=False),
        sa.Column("project_director_user_id", sa.Integer(), nullable=False),
        sa.Column("project_manager_user_id", sa.Integer(), nullable=False),
        sa.Column("delivery_lead_user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["delivery_lead_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_director_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_manager_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["vp_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id", name="uq_project_ownership_project"),
    )
    op.create_index(
        op.f("ix_project_ownership_delivery_lead_user_id"),
        "project_ownership",
        ["delivery_lead_user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_ownership_project_director_user_id"),
        "project_ownership",
        ["project_director_user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_ownership_project_id"),
        "project_ownership",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_ownership_project_manager_user_id"),
        "project_ownership",
        ["project_manager_user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_ownership_vp_user_id"),
        "project_ownership",
        ["vp_user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_project_ownership_vp_user_id"), table_name="project_ownership")
    op.drop_index(op.f("ix_project_ownership_project_manager_user_id"), table_name="project_ownership")
    op.drop_index(op.f("ix_project_ownership_project_id"), table_name="project_ownership")
    op.drop_index(op.f("ix_project_ownership_project_director_user_id"), table_name="project_ownership")
    op.drop_index(op.f("ix_project_ownership_delivery_lead_user_id"), table_name="project_ownership")
    op.drop_table("project_ownership")
    op.drop_index(op.f("ix_projects_name"), table_name="projects")
    op.drop_index(op.f("ix_projects_customer_id"), table_name="projects")
    op.drop_table("projects")
    op.drop_index(op.f("ix_customers_name"), table_name="customers")
    op.drop_table("customers")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
