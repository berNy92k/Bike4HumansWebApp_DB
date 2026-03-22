from typing import List, Annotated

from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.schemas.admin.bike.admin_bike_list_request_dto import BikeListRequestDto
from app.schemas.admin.bike.admin_bike_create_dto import BikeCreateDto
from app.schemas.admin.bike.admin_bike_read_dto import BikeReadDto
from app.schemas.admin.bike.admin_bike_update_dto import BikeUpdateDto
from app.services.admin.admin_bike_service import AdminBikeService

router = APIRouter(
    prefix="/admin/bikes",
    tags=["Admin - bikes"]
)

templates = Jinja2Templates(directory="app/templates")

db_dependency = Annotated[Session, Depends(get_db)]


### Pages ###
@router.get("/list", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_bikes_page(request: Request, db: db_dependency):
    service = AdminBikeService(db)

    page = int(request.query_params.get("page", 1))
    size = int(request.query_params.get("size", 5))

    pagination = service.get_bikes_paginated(BikeListRequestDto(page=page, size=size))

    return templates.TemplateResponse(
        "admin/bikes/bikes.html",
        {
            "request": request,
            "bikes": pagination.items,
            "page": pagination.page,
            "size": pagination.size,
            "total": pagination.total,
            "pages": pagination.pages,
        },
    )


@router.get("/create", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_create_bike(request: Request):
    return templates.TemplateResponse("admin/bikes/bike_create.html", {"request": request})


@router.get("/{bike_id}/details", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_bike_details(request: Request, bike_id: int, db: db_dependency):
    service = AdminBikeService(db)
    bike = service.get_bike_by_id(bike_id)
    return templates.TemplateResponse("admin/bikes/bike_details.html", {"request": request, "bike": bike})


@router.get("/{bike_id}/edit", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_bike_details(request: Request, bike_id: int, db: db_dependency):
    service = AdminBikeService(db)
    bike = service.get_bike_by_id(bike_id)
    return templates.TemplateResponse("admin/bikes/bike_edit.html", {"request": request, "bike": bike})


### ENDPOINTS ###
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[BikeReadDto])
async def find_all_bikes(db: db_dependency):
    service = AdminBikeService(db)
    return service.get_all_bikes()


@router.get("/{bike_id}", status_code=status.HTTP_200_OK, response_model=BikeReadDto)
async def find_bike_by_id(bike_id: int, db: db_dependency):
    service = AdminBikeService(db)
    return service.get_bike_by_id(bike_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_bike(bike_create_dto: BikeCreateDto, db: db_dependency):
    service = AdminBikeService(db)
    service.create_bike(bike_create_dto)


@router.put("/{bike_id}", status_code=status.HTTP_204_NO_CONTENT)
async def create_bike(bike_id: int, bike_update_dto: BikeUpdateDto, db: db_dependency):
    service = AdminBikeService(db)
    service.update_bike_all_fields(bike_id, bike_update_dto)


@router.patch("/{bike_id}", status_code=status.HTTP_204_NO_CONTENT)
async def create_bike(bike_id: int, bike_update_dto: BikeUpdateDto, db: db_dependency):
    service = AdminBikeService(db)
    service.update_bike_separate_fields(bike_id, bike_update_dto)


@router.delete("/{bike_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bike_by_id(bike_id: int, db: db_dependency):
    service = AdminBikeService(db)
    service.delete_bike_by_id(bike_id)
