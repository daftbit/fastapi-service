import os
from fastapi import FastAPI

from src.core.database import Database


def init_api() -> FastAPI:
    """Generates FastAPI instance

    Returns
    -------
    FastAPI
        instance of FastAPI
    """
    version = os.environ.get("VERSION", "1.0.0")
    app = FastAPI(title="FastAPI Service", version=version)
    _init_middleware(app, version)
    # Register event handlers (startup/shutdown)
    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)
    # Register routes

    # Register exception handlers

    return app


def _init_middleware(app: FastAPI, version: str):
    """Initialize all middleware layers

    Parameters
    ----------
    app : FastAPI
    version : str
    """
    # TODO: Add logging formatting here
    pass


def _init_routes(app: FastAPI):
    """Initialize all RESTful API routers

    Parameters
    ----------
    app : FastAPI
    """


async def startup():
    await Database.open_database_connection()


async def shutdown():
    await Database.close_database_connection()
