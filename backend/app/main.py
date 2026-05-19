from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.customers import router as customers_router
from app.api.routes.health import router as health_router
from app.api.routes.project_ownership import router as project_ownership_router
from app.api.routes.projects import router as projects_router
from app.api.routes.users import router as users_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app_name, version=settings.app_version)
    application.include_router(auth_router)
    application.include_router(health_router)
    application.include_router(users_router)
    application.include_router(customers_router)
    application.include_router(projects_router)
    application.include_router(project_ownership_router)
    return application


app = create_app()
