from typing import Annotated, List

from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.schemas.admin.user.admin_user_read_dto import UserReadDto
from app.services.admin.admin_user_service import AdminUserService

router = APIRouter(
    prefix="/admin/user",
    tags=["Admin - user"]
)

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="app/templates")


### Pages ###
@router.get("/list")
async def render_user_page(request: Request, db: db_dependency):
    service = AdminUserService(db)
    users = service.get_all_users()
    return templates.TemplateResponse("admin/users/users.html", {"request": request, "users": users})


### ENDPOINTS ###
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserReadDto])
async def get_all_users(db: db_dependency):
    service = AdminUserService(db)
    return service.get_all_users()
