from typing import List, Annotated

from fastapi import APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.templating import Jinja2Templates

from app.database.database import get_db
from app.schemas.admin.frames.admin_frame_create_dto import FrameCreateDto
from app.schemas.admin.frames.admin_frame_read_dto import FrameReadDto
from app.schemas.admin.frames.admin_frame_update_dto import FrameUpdateDto
from app.services.admin.admin_frame_service import AdminFrameService

router = APIRouter(
    prefix="/admin/frames",
    tags=["Admin - frames"]
)

templates = Jinja2Templates(directory="app/templates")

db_dependency = Annotated[Session, Depends(get_db)]


### Pages ###
@router.get("/list", status_code=status.HTTP_200_OK)
async def render_todo_page(request: Request, db: db_dependency):
    service = AdminFrameService(db)
    bikes = service.get_all_frames()
    return templates.TemplateResponse("admin/frames/frames.html", {"request": request, "bikes": bikes})


### ENDPOINTS ###
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[FrameReadDto])
async def find_all_frames(db: Session = Depends(get_db)):
    service = AdminFrameService(db)
    return service.get_all_frames()


@router.get("/{frame_id}", status_code=status.HTTP_200_OK, response_model=FrameReadDto)
async def find_frame_by_id(frame_id: int, db: Session = Depends(get_db)):
    service = AdminFrameService(db)
    return service.get_frame_by_id(frame_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_frame(frame_create_dto: FrameCreateDto, db: Session = Depends(get_db)):
    service = AdminFrameService(db)
    service.create_frame(frame_create_dto)


@router.put("/{frame_id}", status_code=status.HTTP_204_NO_CONTENT)
async def create_frame(frame_id: int, frame_update_dto: FrameUpdateDto, db: Session = Depends(get_db)):
    service = AdminFrameService(db)
    service.update_frame_all_fields(frame_id, frame_update_dto)


@router.patch("/{frame_id}", status_code=status.HTTP_204_NO_CONTENT)
async def create_frame(frame_id: int, frame_update_dto: FrameUpdateDto, db: Session = Depends(get_db)):
    service = AdminFrameService(db)
    service.update_frame_separate_fields(frame_id, frame_update_dto)


@router.delete("/{frame_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_frame_by_id(frame_id: int, db: Session = Depends(get_db)):
    service = AdminFrameService(db)
    service.delete_frame_by_id(frame_id)
