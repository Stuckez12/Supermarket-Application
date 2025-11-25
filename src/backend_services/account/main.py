from contextlib import asynccontextmanager
from fastapi import FastAPI

from account.common import ACCOUNT_SERVICE_VERSION
from account.routes import app_api

from utils.database import db_connection


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Initialise app
    print("application startup")

    # Starting app
    yield

    # Closing app
    print("application shutdown")


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
