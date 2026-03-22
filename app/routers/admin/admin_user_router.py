from typing import Annotated, List

from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.schemas.admin.user.admin_user_create_dto import UserCreateDto
from app.schemas.admin.user.admin_user_read_dto import UserReadDto
from app.schemas.admin.user.role.admin_role_create_dto import RoleCreateDto
from app.schemas.admin.user.role.admin_role_read_dto import RoleReadDto
from app.schemas.admin.user.role.admin_role_update_dto import RoleUpdateDto
from app.services.admin.admin_user_service import AdminUserService

router = APIRouter(
    prefix="/admin/user",
    tags=["Admin - user"]
)

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="app/templates")


### Pages ###
## USERS ##
@router.get("/list", include_in_schema=False)
async def render_user_page(request: Request, db: db_dependency):
    service = AdminUserService(db)
    users = service.get_all_users()
    return templates.TemplateResponse("admin/users/users.html", {"request": request, "users": users})


@router.get("/create", include_in_schema=False)
async def render_user_create_page(request: Request):
    return templates.TemplateResponse("admin/users/user_create.html", {"request": request})

## ROLES ##
@router.get("/role/list", include_in_schema=False)
async def render_user_page(request: Request, db: db_dependency):
    service = AdminUserService(db)
    roles = service.get_all_roles()
    return templates.TemplateResponse("admin/users/roles/roles.html", {"request": request, "roles": roles})


@router.get("/role/create", include_in_schema=False)
async def render_user_create_page(request: Request):
    return templates.TemplateResponse("admin/users/roles/role_create.html", {"request": request})


@router.get("/role/{role_id}", include_in_schema=False)
async def render_role_details_page(request: Request, role_id: int, db: db_dependency):
    service = AdminUserService(db)
    role = service.get_role_by_id(role_id)
    return templates.TemplateResponse("admin/users/roles/role_details.html", {"request": request, "role": role})


@router.get("/role/{role_id}/edit", include_in_schema=False)
async def render_role_edit_page(request: Request, role_id: int, db: db_dependency):
    service = AdminUserService(db)
    role = service.get_role_by_id(role_id)
    return templates.TemplateResponse("admin/users/roles/role_edit.html", {"request": request, "role": role})


### ENDPOINTS ###
## USERS ##
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserReadDto])
async def get_all_users(db: db_dependency):
    service = AdminUserService(db)
    return service.get_all_users()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreateDto, db: db_dependency):
    service = AdminUserService(db)
    service.create_user(user)

## ROLES ##
@router.get("/roles", status_code=status.HTTP_200_OK, response_model=List[RoleReadDto])
async def get_all_roles(db: db_dependency):
    service = AdminUserService(db)
    return service.get_all_roles()


@router.post("/role", status_code=status.HTTP_201_CREATED)
async def create_new_role(role: RoleCreateDto, db: db_dependency):
    service = AdminUserService(db)
    service.create_role(role)


@router.patch("/role/{role_id}", status_code=status.HTTP_200_OK)
async def update_role_by_id(role_id: int, role: RoleUpdateDto, db: db_dependency):
    service = AdminUserService(db)
    service.update_role_by_id(role_id, role)


@router.delete("/role/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_by_id(role_id: int, db: db_dependency):
    service = AdminUserService(db)
    service.delete_role_by_id(role_id)
