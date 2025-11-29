import logging
import os

from contextlib import asynccontextmanager
from fastapi import FastAPI

from account.common.constants import ACCOUNT_SERVICE_VERSION
from account.common.utils.seed_db import seed_db
from account.routes import app_api

from utils.app_initialise import Initialise
from utils.app_services.account import db_settings, db_url_obj


logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Initialise app
    app_checks = Initialise(db_url_obj, db_settings)
    app_checks.check_database_connection()

    if os.environ.get("PYTHON_ENV") == "production":
        app_checks.database("api/account/alembic.ini")

    seed_db(db_url_obj, db_settings)

    # Starting app
    yield

    # Closing app
    # logger.info("application shutdown there")


def create_app() -> FastAPI:
    app = FastAPI(
        version=ACCOUNT_SERVICE_VERSION,
        debug=True,
        title="Account API",
        description="",
        redirect_slashes=False,
        docs_url="/account/docs",
        lifespan=app_lifespan,
        root_path="/account/v1",
    )

    app.include_router(app_api)

    return app
