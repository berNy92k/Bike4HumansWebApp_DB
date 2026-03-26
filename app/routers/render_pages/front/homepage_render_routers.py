from typing import Annotated

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.services.admin.admin_bike_service import AdminBikeService
from app.services.admin.admin_manufacturer_service import AdminManufacturerService

router = APIRouter(
    include_in_schema=False
)

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def render_homepage(request: Request, db: db_dependency):
    return templates.TemplateResponse("front/homepage/index.html",
                                      {
                                          "request": request,
                                          "bikeSize": len(AdminBikeService(db).get_all_bikes()),
                                          "manufacturerSize": len(AdminManufacturerService(db).get_all_manufacturers())
                                      })
