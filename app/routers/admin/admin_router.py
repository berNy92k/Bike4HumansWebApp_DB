from typing import Annotated

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.services.auth.auth_service import AuthService

router = APIRouter(
    prefix="/admin"
)

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="app/templates")


### Pages ###
@router.get("/")
async def render_admin_homepage(request: Request, db: db_dependency):
    try:
        service = AuthService(db)
        await service.validate_access(request)

        return templates.TemplateResponse("admin/homepage/index.html", {"request": request})
    except HTTPException:
        return redirect_to_login()


def redirect_to_login():
    response = RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response


def redirect_to_homepage():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response
