from typing import List, Annotated

from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.schemas.admin.manufacturers.admin_manufacturer_create_dto import ManufacturerCreateDto
from app.schemas.admin.manufacturers.admin_manufacturer_read_dto import ManufacturerReadDto
from app.schemas.admin.manufacturers.admin_manufacturer_update_dto import ManufacturerUpdateDto
from app.services.admin.admin_manufacturer_service import AdminManufacturerService

router = APIRouter(
    prefix="/admin/manufacturer",
    tags=["Admin - manufacturer"]
)

templates = Jinja2Templates(directory="app/templates")

db_dependency = Annotated[Session, Depends(get_db)]


### Pages ###
@router.get("/list", status_code=status.HTTP_200_OK)
async def render_manufacturer_page(request: Request, db: db_dependency):
    service = AdminManufacturerService(db)
    manufacturers = service.get_all_manufacturers()
    return templates.TemplateResponse("admin/manufacturers/manufacturers.html", {"request": request, "manufacturers": manufacturers})


@router.get("/create", status_code=status.HTTP_200_OK)
async def render_manufacturer_create_page(request: Request):
    return templates.TemplateResponse("admin/manufacturers/manufacturers_create.html", {"request": request})


@router.get("/{manufacturer_id}/details", status_code=status.HTTP_200_OK)
async def render_manufacturer_create_page(request: Request, manufacturer_id: int, db: db_dependency):
    service = AdminManufacturerService(db)
    manufacturer = service.get_manufacturer_by_id(manufacturer_id)
    return templates.TemplateResponse("admin/manufacturers/manufacturers_details.html", {"request": request, "manufacturer": manufacturer})


@router.get("/{manufacturer_id}/edit", status_code=status.HTTP_200_OK)
async def render_manufacturer_create_page(request: Request, manufacturer_id: int, db: db_dependency):
    service = AdminManufacturerService(db)
    manufacturer = service.get_manufacturer_by_id(manufacturer_id)
    return templates.TemplateResponse("admin/manufacturers/manufacturers_edit.html", {"request": request, "manufacturer": manufacturer})


### ENDPOINTS ###
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ManufacturerReadDto])
async def find_all_manufacturers(db: Session = Depends(get_db)):
    service = AdminManufacturerService(db)
    return service.get_all_manufacturers()


@router.get("/{manufacturer_id}", status_code=status.HTTP_200_OK, response_model=ManufacturerReadDto)
async def find_manufacturer_by_id(manufacturer_id: int, db: Session = Depends(get_db)):
    service = AdminManufacturerService(db)
    return service.get_manufacturer_by_id(manufacturer_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_manufacturer(manufacturer_create_dto: ManufacturerCreateDto, db: Session = Depends(get_db)):
    service = AdminManufacturerService(db)
    service.create_manufacturer(manufacturer_create_dto)


@router.put("/{manufacturer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def create_manufacturer(manufacturer_id: int, manufacturer_update_dto: ManufacturerUpdateDto,
                              db: Session = Depends(get_db)):
    service = AdminManufacturerService(db)
    service.update_manufacturer_all_fields(manufacturer_id, manufacturer_update_dto)


@router.patch("/{manufacturer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def create_manufacturer(manufacturer_id: int, manufacturer_update_dto: ManufacturerUpdateDto,
                              db: Session = Depends(get_db)):
    service = AdminManufacturerService(db)
    service.update_manufacturer_separate_fields(manufacturer_id, manufacturer_update_dto)


@router.delete("/{manufacturer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_manufacturer_by_id(manufacturer_id: int, db: Session = Depends(get_db)):
    service = AdminManufacturerService(db)
    service.delete_manufacturer_by_id(manufacturer_id)
