from fastapi import FastAPI

from account.common.constants import ACCOUNT_SERVICE_VERSION


def create_app():
    app = FastAPI(
        version=ACCOUNT_SERVICE_VERSION,
        debug = True,
        title = "Account API",
        description= "",
        redirect_slashes=False,
        docs_url = "/account/docs",

        # on_startup: Sequence[() -> Any] | None = None,
        # on_shutdown: Sequence[() -> Any] | None = None,
        # root_path: str = "",
    )

    @app.get("/ping")
    def root():
        return {"pong": "pong"}
    
    return app
