from typing import Annotated

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.schemas.admin.bike.admin_bike_list_request_dto import BikeListRequestDto
from app.services.admin.admin_manufacturer_service import AdminManufacturerService
from app.services.front.bike_service import BikeService

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
                                          "equipmentShortList": BikeService(db).get_bikes_paginated(BikeListRequestDto(page=1, size=4)),
                                          "bikeSize": len(BikeService(db).get_all_bikes()),
                                          "manufacturerSize": len(AdminManufacturerService(db).get_all_manufacturers())
                                      })
