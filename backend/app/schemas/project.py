from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):
    customer_id: int
    name: str
    health_calculation_enabled: bool = True
    status: str = "active"
    importance: str = "medium"
    is_completed: bool = False
    completed_at: datetime | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    customer_id: int | None = None
    name: str | None = None
    health_calculation_enabled: bool | None = None
    status: str | None = None
    importance: str | None = None
    is_completed: bool | None = None
    completed_at: datetime | None = None


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
