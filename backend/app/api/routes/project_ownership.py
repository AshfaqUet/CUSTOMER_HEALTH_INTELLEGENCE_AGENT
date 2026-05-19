from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.db.session import get_db
from app.models.project_ownership import ProjectOwnership
from app.models.user import User
from app.schemas.project_ownership import (
    ProjectOwnershipCreate,
    ProjectOwnershipRead,
    ProjectOwnershipUpdate,
)
from app.services.ownership import validate_project_ownership
from app.services.rbac import user_can_access_project, visible_project_ownership_statement

router = APIRouter(prefix="/project-ownership", tags=["project ownership"])


def commit_ownership(db: Session, ownership: ProjectOwnership) -> ProjectOwnership:
    try:
        db.add(ownership)
        db.commit()
        db.refresh(ownership)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Each project can have only one ownership record.",
        ) from exc
    return ownership


@router.post("", response_model=ProjectOwnershipRead, status_code=status.HTTP_201_CREATED)
def create_project_ownership(
    payload: ProjectOwnershipCreate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> ProjectOwnership:
    validate_project_ownership(db, **payload.model_dump())
    ownership = ProjectOwnership(**payload.model_dump())
    return commit_ownership(db, ownership)


@router.get("", response_model=list[ProjectOwnershipRead])
def list_project_ownership(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[ProjectOwnership]:
    return list(db.scalars(visible_project_ownership_statement(current_user)).all())


@router.get("/{ownership_id}", response_model=ProjectOwnershipRead)
def read_project_ownership(
    ownership_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProjectOwnership:
    ownership = db.get(ProjectOwnership, ownership_id)
    if ownership is None or not user_can_access_project(db, current_user, ownership.project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project ownership not found.",
        )
    return ownership


@router.patch("/{ownership_id}", response_model=ProjectOwnershipRead)
def update_project_ownership(
    ownership_id: int,
    payload: ProjectOwnershipUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> ProjectOwnership:
    ownership = db.get(ProjectOwnership, ownership_id)
    if ownership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project ownership not found.",
        )

    update_data = payload.model_dump(exclude_unset=True)
    merged = {
        "project_id": ownership.project_id,
        "vp_user_id": ownership.vp_user_id,
        "project_director_user_id": ownership.project_director_user_id,
        "project_manager_user_id": ownership.project_manager_user_id,
        "delivery_lead_user_id": ownership.delivery_lead_user_id,
    }
    merged.update(update_data)
    validate_project_ownership(db, ownership_id=ownership.id, **merged)

    for field, value in update_data.items():
        setattr(ownership, field, value)

    return commit_ownership(db, ownership)
