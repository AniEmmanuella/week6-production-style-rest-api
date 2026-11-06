from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models import Task  # noqa: F401 - registers ORM model metadata
from app.api.routes import health, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "A modular task-management REST API demonstrating FastAPI, Pydantic, "
        "SQLAlchemy, CRUD, pagination, filtering, Bearer-token authentication and tests."
    ),
    debug=settings.debug,
    lifespan=lifespan,
)


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred. Please try again later."},
    )


app.include_router(health.router)
app.include_router(tasks.router, prefix=settings.api_prefix)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the Week 6 REST API",
        "docs": "/docs",
        "health": "/health",
    }
