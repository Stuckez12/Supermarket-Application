from fastapi import FastAPI

from gateway.common.apis import router


def start_server():
    app = FastAPI(
        debug=True,
        title="Gateway API",
        summary="Gateway server to the application services",
        description="A gateway between the client and many different servers",
        version="0.0.1",
        deprecated=False,
    )

    app.include_router(router)

    return app
