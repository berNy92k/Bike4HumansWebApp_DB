from typing import Annotated

from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.schemas.admin.manufacturers.admin_manufacturer_list_request_dto import ManufacturerListRequestDto
from app.services.admin.admin_manufacturer_service import AdminManufacturerService

router = APIRouter(
    prefix="/admin/manufacturer",
    tags=["Admin - manufacturer"]
)

templates = Jinja2Templates(directory="app/templates")

db_dependency = Annotated[Session, Depends(get_db)]


### Pages ###
@router.get("/list", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_manufacturer_page(request: Request, db: db_dependency):
    service = AdminManufacturerService(db)

    page = int(request.query_params.get("page", 1))
    size = int(request.query_params.get("size", 5))

    pagination = service.get_manufacturers_paginated(
        ManufacturerListRequestDto(page=page, size=size)
    )

    return templates.TemplateResponse(
        "admin/manufacturers/manufacturers.html",
        {
            "request": request,
            "manufacturers": pagination.items,
            "page": pagination.page,
            "size": pagination.size,
            "total": pagination.total,
            "pages": pagination.pages,
        },
    )


@router.get("/create", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_manufacturer_create_page(request: Request):
    return templates.TemplateResponse("admin/manufacturers/manufacturers_create.html", {"request": request})


@router.get("/{manufacturer_id}/details", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_manufacturer_create_page(request: Request, manufacturer_id: int, db: db_dependency):
    service = AdminManufacturerService(db)
    manufacturer = service.get_manufacturer_by_id(manufacturer_id)
    return templates.TemplateResponse("admin/manufacturers/manufacturers_details.html",
                                      {"request": request, "manufacturer": manufacturer})


@router.get("/{manufacturer_id}/edit", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_manufacturer_create_page(request: Request, manufacturer_id: int, db: db_dependency):
    service = AdminManufacturerService(db)
    manufacturer = service.get_manufacturer_by_id(manufacturer_id)
    return templates.TemplateResponse("admin/manufacturers/manufacturers_edit.html",
                                      {"request": request, "manufacturer": manufacturer})
