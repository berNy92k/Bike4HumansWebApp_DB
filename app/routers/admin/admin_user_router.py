from typing import Annotated, List

from fastapi import APIRouter, Request, Query
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.schemas.admin.user.admin_user_create_dto import UserCreateDto
from app.schemas.admin.user.admin_user_list_request_dto import UserListRequestDto
from app.schemas.admin.user.admin_user_read_dto import UserReadDto
from app.schemas.admin.user.admin_user_update_dto import UserUpdateDto
from app.schemas.admin.user.role.admin_role_create_dto import RoleCreateDto
from app.schemas.admin.user.role.admin_role_list_request_dto import RoleListRequestDto
from app.schemas.admin.user.role.admin_role_list_response_dto import RoleListResponseDto
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
@router.get("/list", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_user_page(request: Request, db: db_dependency):
    service = AdminUserService(db)

    page = int(request.query_params.get("page", 1))
    size = int(request.query_params.get("size", 5))

    pagination = service.get_users_paginated(UserListRequestDto(page=page, size=size))

    return templates.TemplateResponse(
        "admin/users/users.html",
        {
            "request": request,
            "users": pagination.items,
            "page": pagination.page,
            "size": pagination.size,
            "total": pagination.total,
            "pages": pagination.pages,
        },
    )


@router.get("/create", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_user_create_page(request: Request, db: db_dependency):
    service = AdminUserService(db)
    roles = service.get_all_roles()
    return templates.TemplateResponse("admin/users/user_create.html", {"request": request, "roles": roles})


@router.get("/{user_id}/details", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_user_details_page(request: Request, user_id: int, db: db_dependency):
    service = AdminUserService(db)
    user = service.get_user_by_id(user_id)
    return templates.TemplateResponse("admin/users/user_details.html", {"request": request, "user": user})


@router.get("/{user_id}/edit", status_code=status.HTTP_200_OK, include_in_schema=False)
async def render_user_edit_page(request: Request, user_id: int, db: db_dependency):
    service = AdminUserService(db)
    user = service.get_user_by_id(user_id)
    roles = service.get_all_roles()
    return templates.TemplateResponse("admin/users/user_edit.html", {"request": request, "user": user, "roles": roles})


## ROLES ##
@router.get("/role/list", include_in_schema=False)
async def render_role_list_page(request: Request, db: db_dependency):
    service = AdminUserService(db)

    page = int(request.query_params.get("page", 1))
    size = int(request.query_params.get("size", 5))

    pagination = service.get_roles_paginated(RoleListRequestDto(page=page, size=size))

    return templates.TemplateResponse(
        "admin/users/roles/roles.html",
        {
            "request": request,
            "roles": pagination.items,
            "page": pagination.page,
            "size": pagination.size,
            "total": pagination.total,
            "pages": pagination.pages,
        }
    )


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


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_new_user(user_id: int, user_update_dto: UserUpdateDto, db: db_dependency):
    service = AdminUserService(db)
    service.update_user_all_fields(user_id, user_update_dto)


## ROLES ##
@router.get("/roles", status_code=status.HTTP_200_OK, response_model=RoleListResponseDto)
async def get_all_roles(db: db_dependency, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
    service = AdminUserService(db)
    return service.get_roles_paginated(RoleListRequestDto(page=page, size=size))


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
