from typing import Annotated

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.routers.utils.admin_utils_router import redirect_to_login
from app.services.auth.auth_service import AuthService

router = APIRouter(
    prefix="/admin",
    include_in_schema=False
)

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="app/templates")


### Pages ###
@router.get("/")
async def render_admin_homepage(request: Request, db: db_dependency):
    try:
        await AuthService(db).validate_access(request)



        return templates.TemplateResponse("admin/homepage/index.html", {"request": request})
    except HTTPException:
        return redirect_to_login()