from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from app.database.database import Base, engine
# from app.models.role import Role
# from app.models.user import User
from app.routers.admin import admin_bike_router, admin_manufacturers_router, admin_user_router, admin_router
from app.routers.auth import auth_router
from app.routers.front import homepage_router

app = FastAPI()

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

# @app.on_event("startup")
# def on_startup():
#     Base.metadata.create_all(bind=engine)
