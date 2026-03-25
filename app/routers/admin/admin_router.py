from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/admin")
async def render_admin_homepage(request: Request):
    return templates.TemplateResponse("admin/homepage/index.html", {"request": request})
