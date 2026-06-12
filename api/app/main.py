from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings
from app.health import router as health_router
from app.postgres import PostgresReadiness


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(title="Finance System API")
    app.state.readiness_check = PostgresReadiness(
        database_url=settings.database_url,
        timeout_seconds=settings.db_readiness_timeout_seconds,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app.include_router(health_router)
    return app


app = create_app()
