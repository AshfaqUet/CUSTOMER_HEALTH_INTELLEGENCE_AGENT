from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class ProjectOwnership(TimestampMixin, Base):
    __tablename__ = "project_ownership"
    __table_args__ = (UniqueConstraint("project_id", name="uq_project_ownership_project"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    vp_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    project_director_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    project_manager_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    delivery_lead_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    project = relationship("Project", back_populates="ownership")
    vp_user = relationship(
        "User",
        back_populates="vp_project_ownerships",
        foreign_keys=[vp_user_id],
    )
    project_director_user = relationship(
        "User",
        back_populates="director_project_ownerships",
        foreign_keys=[project_director_user_id],
    )
    project_manager_user = relationship(
        "User",
        back_populates="manager_project_ownerships",
        foreign_keys=[project_manager_user_id],
    )
    delivery_lead_user = relationship(
        "User",
        back_populates="delivery_lead_project_ownerships",
        foreign_keys=[delivery_lead_user_id],
    )
