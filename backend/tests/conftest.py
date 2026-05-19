from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import Customer, Project, ProjectOwnership, User, UserRole


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as session:
        yield session

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def create_user(
    db: Session,
    role: UserRole,
    email: str,
    name: str | None = None,
) -> User:
    user = User(
        name=name or email.split("@")[0],
        email=email,
        role=role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_customer(db: Session, name: str = "Customer") -> Customer:
    customer = Customer(name=name, priority="medium", status="active")
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def create_project(
    db: Session,
    customer: Customer,
    name: str,
    is_completed: bool = False,
) -> Project:
    project = Project(
        customer_id=customer.id,
        name=name,
        status="completed" if is_completed else "active",
        importance="medium",
        is_completed=is_completed,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def create_ownership(
    db: Session,
    project: Project,
    vp: User,
    director: User,
    manager: User,
    delivery_lead: User,
) -> ProjectOwnership:
    ownership = ProjectOwnership(
        project_id=project.id,
        vp_user_id=vp.id,
        project_director_user_id=director.id,
        project_manager_user_id=manager.id,
        delivery_lead_user_id=delivery_lead.id,
    )
    db.add(ownership)
    db.commit()
    db.refresh(ownership)
    return ownership


def auth_headers(user: User) -> dict[str, str]:
    return {"X-User-Id": str(user.id)}
