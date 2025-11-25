from fastapi import APIRouter

from account.routes.root import api as root_api


all_routers = [root_api]

app_api = APIRouter()

for route in all_routers:
    app_api.include_router(route)
