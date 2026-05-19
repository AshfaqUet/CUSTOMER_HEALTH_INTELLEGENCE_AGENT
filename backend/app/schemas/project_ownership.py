from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectOwnershipBase(BaseModel):
    project_id: int
    vp_user_id: int
    project_director_user_id: int
    project_manager_user_id: int
    delivery_lead_user_id: int


class ProjectOwnershipCreate(ProjectOwnershipBase):
    pass


class ProjectOwnershipUpdate(BaseModel):
    vp_user_id: int | None = None
    project_director_user_id: int | None = None
    project_manager_user_id: int | None = None
    delivery_lead_user_id: int | None = None


class ProjectOwnershipRead(ProjectOwnershipBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
