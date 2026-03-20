from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database.database import Base, engine
from app.routers.admin import admin_bike_router, admin_manufacturers_router, admin_user_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(admin_user_router.router)
app.include_router(admin_bike_router.router)
app.include_router(admin_manufacturers_router.router)

templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def render_homepage(request: Request):
    return templates.TemplateResponse("front/homepage/index.html", {"request": request})

@app.get("/admin")
async def render_admin_homepage(request: Request):
    return templates.TemplateResponse("admin/homepage/index.html", {"request": request})
