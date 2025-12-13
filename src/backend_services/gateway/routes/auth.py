from fastapi import APIRouter, Request


api = APIRouter(prefix="/auth", tags=["Account"])


@api.post(
    path="/account/register",
    response_model=None,
    name="Account Registration",
    description="Gateway to account service to register an account on the application",
)
def post_account_registration(request: Request):
    pass


@api.post(
    path="/account/login",
    response_model=None,
    name="Account Login",
    description="Gateway to account service to log in to the application",
)
def post_account_login(request: Request):
    pass
