from fastapi import APIRouter

from account.schemas import ApplicationHealth


api = APIRouter(
    prefix="",
    tags=["users", "authentication"],
    redirect_slashes=False,
)


@api.get("/health")
def get_app_health():
    return ApplicationHealth(db=True)
