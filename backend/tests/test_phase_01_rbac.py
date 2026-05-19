from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import UserRole
from tests.conftest import (
    auth_headers,
    create_customer,
    create_ownership,
    create_project,
    create_user,
)


def test_user_role_validation_rejects_invalid_role(
    client: TestClient,
    db_session: Session,
) -> None:
    admin = create_user(db_session, UserRole.ADMIN, "admin@example.com")

    response = client.post(
        "/users",
        headers=auth_headers(admin),
        json={
            "name": "Invalid Role",
            "email": "invalid@example.com",
            "role": "not_a_role",
            "is_active": True,
        },
    )

    assert response.status_code == 422


def test_first_user_can_be_bootstrapped_as_admin_without_header(
    client: TestClient,
) -> None:
    response = client.post(
        "/users",
        json={
            "name": "Bootstrap Admin",
            "email": "bootstrap@example.com",
            "role": "admin",
            "is_active": True,
        },
    )

    assert response.status_code == 201
    assert response.json()["role"] == "admin"


def test_first_user_must_be_admin(client: TestClient) -> None:
    response = client.post(
        "/users",
        json={
            "name": "Not Admin",
            "email": "not-admin@example.com",
            "role": "project_manager",
            "is_active": True,
        },
    )

    assert response.status_code == 400
    assert "first user must be an admin" in response.json()["detail"].lower()


def test_duplicate_user_email_is_rejected(
    client: TestClient,
    db_session: Session,
) -> None:
    admin = create_user(db_session, UserRole.ADMIN, "admin@example.com")
    create_user(db_session, UserRole.PROJECT_MANAGER, "duplicate@example.com")

    response = client.post(
        "/users",
        headers=auth_headers(admin),
        json={
            "name": "Duplicate",
            "email": "duplicate@example.com",
            "role": "project_manager",
            "is_active": True,
        },
    )

    assert response.status_code == 400
    assert "unique" in response.json()["detail"]


def test_current_user_simulation_returns_authenticated_user(
    client: TestClient,
    db_session: Session,
) -> None:
    admin = create_user(db_session, UserRole.ADMIN, "admin@example.com")

    response = client.get("/auth/current-user", headers=auth_headers(admin))

    assert response.status_code == 200
    assert response.json()["email"] == "admin@example.com"


def test_non_admin_cannot_create_customer(
    client: TestClient,
    db_session: Session,
) -> None:
    project_manager = create_user(
        db_session,
        UserRole.PROJECT_MANAGER,
        "manager@example.com",
    )

    response = client.post(
        "/customers",
        headers=auth_headers(project_manager),
        json={"name": "Forbidden Customer"},
    )

    assert response.status_code == 403


def test_admin_can_create_customer(client: TestClient, db_session: Session) -> None:
    admin = create_user(db_session, UserRole.ADMIN, "admin@example.com")

    response = client.post(
        "/customers",
        headers=auth_headers(admin),
        json={"name": "Acme", "priority": "high", "status": "active"},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Acme"


def test_admin_can_create_project(client: TestClient, db_session: Session) -> None:
    admin = create_user(db_session, UserRole.ADMIN, "admin@example.com")
    customer = create_customer(db_session, "Acme")

    response = client.post(
        "/projects",
        headers=auth_headers(admin),
        json={"customer_id": customer.id, "name": "Implementation"},
    )

    assert response.status_code == 201
    assert response.json()["customer_id"] == customer.id
    assert response.json()["name"] == "Implementation"


def test_admin_can_assign_required_project_owners(
    client: TestClient,
    db_session: Session,
) -> None:
    admin = create_user(db_session, UserRole.ADMIN, "admin@example.com")
    vp = create_user(db_session, UserRole.VICE_PRESIDENT, "vp@example.com")
    director = create_user(db_session, UserRole.PROJECT_DIRECTOR, "director@example.com")
    manager = create_user(db_session, UserRole.PROJECT_MANAGER, "manager@example.com")
    delivery_lead = create_user(db_session, UserRole.DELIVERY_LEAD, "dl@example.com")
    customer = create_customer(db_session, "Acme")
    project = create_project(db_session, customer, "Implementation")

    response = client.post(
        "/project-ownership",
        headers=auth_headers(admin),
        json={
            "project_id": project.id,
            "vp_user_id": vp.id,
            "project_director_user_id": director.id,
            "project_manager_user_id": manager.id,
            "delivery_lead_user_id": delivery_lead.id,
        },
    )

    assert response.status_code == 201
    assert response.json()["project_id"] == project.id
    assert response.json()["delivery_lead_user_id"] == delivery_lead.id


def test_project_ownership_rejects_owner_with_wrong_role(
    client: TestClient,
    db_session: Session,
) -> None:
    admin = create_user(db_session, UserRole.ADMIN, "admin@example.com")
    wrong_vp = create_user(db_session, UserRole.PROJECT_MANAGER, "wrong-vp@example.com")
    director = create_user(db_session, UserRole.PROJECT_DIRECTOR, "director@example.com")
    manager = create_user(db_session, UserRole.PROJECT_MANAGER, "manager@example.com")
    delivery_lead = create_user(db_session, UserRole.DELIVERY_LEAD, "dl@example.com")
    customer = create_customer(db_session, "Acme")
    project = create_project(db_session, customer, "Implementation")

    response = client.post(
        "/project-ownership",
        headers=auth_headers(admin),
        json={
            "project_id": project.id,
            "vp_user_id": wrong_vp.id,
            "project_director_user_id": director.id,
            "project_manager_user_id": manager.id,
            "delivery_lead_user_id": delivery_lead.id,
        },
    )

    assert response.status_code == 400
    assert "vice_president" in response.json()["detail"]


def test_assigning_same_delivery_lead_to_two_active_projects_is_blocked(
    client: TestClient,
    db_session: Session,
) -> None:
    admin = create_user(db_session, UserRole.ADMIN, "admin@example.com")
    vp = create_user(db_session, UserRole.VICE_PRESIDENT, "vp@example.com")
    director = create_user(db_session, UserRole.PROJECT_DIRECTOR, "director@example.com")
    manager = create_user(db_session, UserRole.PROJECT_MANAGER, "manager@example.com")
    delivery_lead = create_user(db_session, UserRole.DELIVERY_LEAD, "dl@example.com")
    customer = create_customer(db_session, "Acme")
    first_project = create_project(db_session, customer, "First")
    second_project = create_project(db_session, customer, "Second")
    create_ownership(db_session, first_project, vp, director, manager, delivery_lead)

    response = client.post(
        "/project-ownership",
        headers=auth_headers(admin),
        json={
            "project_id": second_project.id,
            "vp_user_id": vp.id,
            "project_director_user_id": director.id,
            "project_manager_user_id": manager.id,
            "delivery_lead_user_id": delivery_lead.id,
        },
    )

    assert response.status_code == 400
    assert "already assigned" in response.json()["detail"]


def test_completed_project_assignment_does_not_block_active_delivery_lead_assignment(
    client: TestClient,
    db_session: Session,
) -> None:
    admin = create_user(db_session, UserRole.ADMIN, "admin@example.com")
    vp = create_user(db_session, UserRole.VICE_PRESIDENT, "vp@example.com")
    director = create_user(db_session, UserRole.PROJECT_DIRECTOR, "director@example.com")
    manager = create_user(db_session, UserRole.PROJECT_MANAGER, "manager@example.com")
    delivery_lead = create_user(db_session, UserRole.DELIVERY_LEAD, "dl@example.com")
    customer = create_customer(db_session, "Acme")
    completed_project = create_project(db_session, customer, "Completed", is_completed=True)
    active_project = create_project(db_session, customer, "Active")
    create_ownership(db_session, completed_project, vp, director, manager, delivery_lead)

    response = client.post(
        "/project-ownership",
        headers=auth_headers(admin),
        json={
            "project_id": active_project.id,
            "vp_user_id": vp.id,
            "project_director_user_id": director.id,
            "project_manager_user_id": manager.id,
            "delivery_lead_user_id": delivery_lead.id,
        },
    )

    assert response.status_code == 201
    assert response.json()["project_id"] == active_project.id


def test_admin_can_see_all_projects(client: TestClient, db_session: Session) -> None:
    admin = create_user(db_session, UserRole.ADMIN, "admin@example.com")
    customer = create_customer(db_session, "Acme")
    first_project = create_project(db_session, customer, "First")
    second_project = create_project(db_session, customer, "Second")

    response = client.get("/projects", headers=auth_headers(admin))

    assert response.status_code == 200
    assert [project["id"] for project in response.json()] == [
        first_project.id,
        second_project.id,
    ]


def test_vp_sees_only_assigned_projects(client: TestClient, db_session: Session) -> None:
    context = seed_two_owned_projects(db_session)

    response = client.get("/projects", headers=auth_headers(context["vp_one"]))

    assert response.status_code == 200
    assert [project["id"] for project in response.json()] == [context["project_one"].id]


def test_vp_sees_only_customers_for_assigned_projects(
    client: TestClient,
    db_session: Session,
) -> None:
    context = seed_two_owned_projects(db_session)

    response = client.get("/customers", headers=auth_headers(context["vp_one"]))

    assert response.status_code == 200
    assert [customer["id"] for customer in response.json()] == [context["customer_one"].id]


def test_project_director_sees_only_assigned_projects(
    client: TestClient,
    db_session: Session,
) -> None:
    context = seed_two_owned_projects(db_session)

    response = client.get("/projects", headers=auth_headers(context["director_one"]))

    assert response.status_code == 200
    assert [project["id"] for project in response.json()] == [context["project_one"].id]


def test_project_manager_sees_only_assigned_projects(
    client: TestClient,
    db_session: Session,
) -> None:
    context = seed_two_owned_projects(db_session)

    response = client.get("/projects", headers=auth_headers(context["manager_one"]))

    assert response.status_code == 200
    assert [project["id"] for project in response.json()] == [context["project_one"].id]


def test_delivery_lead_sees_only_assigned_project(
    client: TestClient,
    db_session: Session,
) -> None:
    context = seed_two_owned_projects(db_session)

    response = client.get("/projects", headers=auth_headers(context["dl_one"]))

    assert response.status_code == 200
    assert [project["id"] for project in response.json()] == [context["project_one"].id]


def seed_two_owned_projects(db: Session):
    customer_one = create_customer(db, "Acme")
    customer_two = create_customer(db, "Globex")
    project_one = create_project(db, customer_one, "First")
    project_two = create_project(db, customer_two, "Second")
    vp_one = create_user(db, UserRole.VICE_PRESIDENT, "vp-one@example.com")
    vp_two = create_user(db, UserRole.VICE_PRESIDENT, "vp-two@example.com")
    director_one = create_user(db, UserRole.PROJECT_DIRECTOR, "director-one@example.com")
    director_two = create_user(db, UserRole.PROJECT_DIRECTOR, "director-two@example.com")
    manager_one = create_user(db, UserRole.PROJECT_MANAGER, "manager-one@example.com")
    manager_two = create_user(db, UserRole.PROJECT_MANAGER, "manager-two@example.com")
    dl_one = create_user(db, UserRole.DELIVERY_LEAD, "dl-one@example.com")
    dl_two = create_user(db, UserRole.DELIVERY_LEAD, "dl-two@example.com")

    create_ownership(db, project_one, vp_one, director_one, manager_one, dl_one)
    create_ownership(db, project_two, vp_two, director_two, manager_two, dl_two)

    return {
        "customer_one": customer_one,
        "customer_two": customer_two,
        "project_one": project_one,
        "project_two": project_two,
        "vp_one": vp_one,
        "director_one": director_one,
        "manager_one": manager_one,
        "dl_one": dl_one,
    }
