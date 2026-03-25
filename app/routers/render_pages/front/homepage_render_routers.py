from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def render_homepage(request: Request):
    return templates.TemplateResponse("front/homepage/index.html", {"request": request})
