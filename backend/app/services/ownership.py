from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_ownership import ProjectOwnership
from app.models.user import User, UserRole

ROLE_REQUIREMENTS = {
    "vp_user_id": UserRole.VICE_PRESIDENT,
    "project_director_user_id": UserRole.PROJECT_DIRECTOR,
    "project_manager_user_id": UserRole.PROJECT_MANAGER,
    "delivery_lead_user_id": UserRole.DELIVERY_LEAD,
}


def ensure_project_exists(db: Session, project_id: int) -> Project:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )
    return project


def ensure_user_has_role(db: Session, field_name: str, user_id: int) -> User:
    user = db.get(User, user_id)
    required_role = ROLE_REQUIREMENTS[field_name]
    if user is None or not user.is_active or user.role != required_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} must reference an active {required_role.value} user.",
        )
    return user


def ensure_delivery_lead_available(
    db: Session,
    project: Project,
    delivery_lead_user_id: int,
    ownership_id: int | None = None,
) -> None:
    if project.is_completed:
        return

    statement = (
        select(ProjectOwnership)
        .join(Project)
        .where(
            ProjectOwnership.delivery_lead_user_id == delivery_lead_user_id,
            Project.is_completed.is_(False),
            ProjectOwnership.project_id != project.id,
        )
    )
    if ownership_id is not None:
        statement = statement.where(ProjectOwnership.id != ownership_id)

    existing = db.scalars(statement).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Delivery Lead is already assigned to another active project.",
        )


def validate_project_ownership(
    db: Session,
    project_id: int,
    vp_user_id: int,
    project_director_user_id: int,
    project_manager_user_id: int,
    delivery_lead_user_id: int,
    ownership_id: int | None = None,
) -> Project:
    project = ensure_project_exists(db, project_id)
    ensure_user_has_role(db, "vp_user_id", vp_user_id)
    ensure_user_has_role(db, "project_director_user_id", project_director_user_id)
    ensure_user_has_role(db, "project_manager_user_id", project_manager_user_id)
    ensure_user_has_role(db, "delivery_lead_user_id", delivery_lead_user_id)
    ensure_delivery_lead_available(db, project, delivery_lead_user_id, ownership_id)
    return project
