from fastapi import APIRouter

from gateway.routes import auth

router = APIRouter()
router.include_router(auth.api)
