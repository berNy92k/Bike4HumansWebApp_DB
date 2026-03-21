from typing import Annotated, List

from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.schemas.admin.user.admin_user_create_dto import UserCreateDto
from app.schemas.admin.user.admin_user_read_dto import UserReadDto
from app.services.admin.admin_user_service import AdminUserService

router = APIRouter(
    prefix="/admin/user",
    tags=["Admin - user"]
)

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="app/templates")


### Pages ###
@router.get("/list", include_in_schema=False)
async def render_user_page(request: Request, db: db_dependency):
    service = AdminUserService(db)
    users = service.get_all_users()
    return templates.TemplateResponse("admin/users/users.html", {"request": request, "users": users})


@router.get("/create", include_in_schema=False)
async def render_user_create_page(request: Request):
    return templates.TemplateResponse("admin/users/user_create.html", {"request": request})


### ENDPOINTS ###
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserReadDto])
async def get_all_users(db: db_dependency):
    service = AdminUserService(db)
    return service.get_all_users()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreateDto, db: db_dependency):
    service = AdminUserService(db)
    service.create_user(user)
