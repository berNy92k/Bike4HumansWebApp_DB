from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.routers.admin import admin_bike_router, admin_manufacturers_router, admin_user_router, admin_router
from app.routers.auth import auth_router
from app.routers.front import homepage_router


def init_routers(app: FastAPI):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # front
    app.include_router(homepage_router.router)

    # auth
    app.include_router(auth_router.router)

    # front
    app.include_router(admin_router.router)
    app.include_router(admin_user_router.router)
    app.include_router(admin_bike_router.router)
    app.include_router(admin_manufacturers_router.router)
