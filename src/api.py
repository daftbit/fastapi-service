import os
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.core.database import Database
from src.core.exceptions.exception import DatabaseException, NotFoundException
from src.core.exceptions.exception_handler import (
    database_exception_handler,
    resource_not_found_exception_handler,
    validation_exception_handler,
)
from src.routes.organization import organization
from src.routes.client import client


def init_api() -> FastAPI:
    """Generates FastAPI instance

    Returns
    -------
    FastAPI
        instance of FastAPI
    """
    version = os.environ.get("VERSION", "1.0.0")
    app = FastAPI(title="FastAPI Service", version=version)
    # Register middleware
    _init_middleware(app, version)
    # Register routes
    _init_routes(app)
    # Register event handlers (startup/shutdown)
    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)
    # Register exception handlers
    _init_exception_handlers(app)

    return app


def _init_middleware(app: FastAPI, version: str):
    """Initialize all middleware layers

    Parameters
    ----------
    app : FastAPI
    version : str
    """
    # TODO: Add logging formatting here and any other middleware
    pass


def _init_routes(app: FastAPI):
    """Initialize all RESTful API routers

    Parameters
    ----------
    app : FastAPI
    """
    app.include_router(organization, prefix="/v1")
    app.include_router(client, prefix="/v1")


def _init_exception_handlers(app: FastAPI):
    """Initialize all exception handlers

    Parameters
    ----------
    app : FastAPI
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(NotFoundException, resource_not_found_exception_handler)
    app.add_exception_handler(DatabaseException, database_exception_handler)


async def startup():
    """Startup event registered to app"""
    await Database.open_database_connection()


async def shutdown():
    """Shutdown event registered to app"""
    await Database.close_database_connection()
