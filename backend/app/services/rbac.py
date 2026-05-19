from sqlalchemy import Select, exists, select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.project import Project
from app.models.project_ownership import ProjectOwnership
from app.models.user import User, UserRole


def project_visibility_filter(user: User):
    if user.role == UserRole.VICE_PRESIDENT:
        return ProjectOwnership.vp_user_id == user.id
    if user.role == UserRole.PROJECT_DIRECTOR:
        return ProjectOwnership.project_director_user_id == user.id
    if user.role == UserRole.PROJECT_MANAGER:
        return ProjectOwnership.project_manager_user_id == user.id
    if user.role == UserRole.DELIVERY_LEAD:
        return ProjectOwnership.delivery_lead_user_id == user.id
    return None


def visible_projects_statement(user: User) -> Select[tuple[Project]]:
    statement = select(Project).order_by(Project.id)
    if user.role == UserRole.ADMIN:
        return statement

    visibility_filter = project_visibility_filter(user)
    if visibility_filter is None:
        return statement.where(False)

    return statement.join(ProjectOwnership).where(visibility_filter)


def visible_customers_statement(user: User) -> Select[tuple[Customer]]:
    statement = select(Customer).order_by(Customer.id)
    if user.role == UserRole.ADMIN:
        return statement

    visibility_filter = project_visibility_filter(user)
    if visibility_filter is None:
        return statement.where(False)

    return (
        statement.join(Project)
        .join(ProjectOwnership)
        .where(visibility_filter)
        .distinct()
    )


def visible_project_ownership_statement(user: User) -> Select[tuple[ProjectOwnership]]:
    statement = select(ProjectOwnership).order_by(ProjectOwnership.id)
    if user.role == UserRole.ADMIN:
        return statement

    visibility_filter = project_visibility_filter(user)
    if visibility_filter is None:
        return statement.where(False)

    return statement.where(visibility_filter)


def user_can_access_project(db: Session, user: User, project_id: int) -> bool:
    if user.role == UserRole.ADMIN:
        return db.get(Project, project_id) is not None

    visibility_filter = project_visibility_filter(user)
    if visibility_filter is None:
        return False

    return db.scalar(
        select(
            exists().where(
                ProjectOwnership.project_id == project_id,
                visibility_filter,
            )
        )
    )
