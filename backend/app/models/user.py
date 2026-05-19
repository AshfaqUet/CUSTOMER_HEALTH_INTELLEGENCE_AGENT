from enum import Enum

from sqlalchemy import Boolean, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class UserRole(str, Enum):
    ADMIN = "admin"
    VICE_PRESIDENT = "vice_president"
    PROJECT_DIRECTOR = "project_director"
    PROJECT_MANAGER = "project_manager"
    DELIVERY_LEAD = "delivery_lead"


def enum_values(enum_type: type[Enum]) -> list[str]:
    return [item.value for item in enum_type]


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(
            UserRole,
            values_callable=enum_values,
            native_enum=False,
            create_constraint=True,
            length=32,
        ),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    vp_project_ownerships = relationship(
        "ProjectOwnership",
        back_populates="vp_user",
        foreign_keys="ProjectOwnership.vp_user_id",
    )
    director_project_ownerships = relationship(
        "ProjectOwnership",
        back_populates="project_director_user",
        foreign_keys="ProjectOwnership.project_director_user_id",
    )
    manager_project_ownerships = relationship(
        "ProjectOwnership",
        back_populates="project_manager_user",
        foreign_keys="ProjectOwnership.project_manager_user_id",
    )
    delivery_lead_project_ownerships = relationship(
        "ProjectOwnership",
        back_populates="delivery_lead_user",
        foreign_keys="ProjectOwnership.delivery_lead_user_id",
    )
